'use client'

import { useState, useEffect, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
    Cloud, Droplets, Thermometer, Sprout, ShieldAlert,
    FlaskConical, Calendar, MapPin, Play, Volume2,
    ShoppingCart, Info, TrendingUp, Landmark, Wind
} from "lucide-react"
import api from "@/lib/api"

export default function AdvisoryPage() {
    const [location, setLocation] = useState<{ lat: number, lon: number } | null>(null)
    const [crop, setCrop] = useState("Tomato")
    const [stage, setStage] = useState("Vegetative")
    const [advisory, setAdvisory] = useState<any>(null)
    const [loading, setLoading] = useState(false)
    const [isSpeaking, setIsSpeaking] = useState(false)

    const fetchAdvisory = useCallback(async (lat: number, lon: number, currentCrop: string, currentStage: string) => {
        setLoading(true)
        try {
            const res = await api.post("/advisory/get-advice", {
                lat,
                lon,
                crop_name: currentCrop,
                growth_stage: currentStage
            })
            setAdvisory(res.data)
        } catch (error) {
            console.error("Failed to fetch advisory", error)
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const { latitude, longitude } = pos.coords
                    setLocation({ lat: latitude, lon: longitude })
                    fetchAdvisory(latitude, longitude, crop, stage)
                },
                (err) => {
                    console.error("Location error", err)
                    // Default to Pune coordinates if GPS fails for demo
                    const lat = 18.5204, lon = 73.8567
                    setLocation({ lat, lon })
                    fetchAdvisory(lat, lon, crop, stage)
                }
            )
        }
    }, [])

    const handleUpdate = () => {
        if (location) {
            fetchAdvisory(location.lat, location.lon, crop, stage)
        }
    }

    const speakAdvisory = () => {
        if (!advisory?.voice_advice) return

        // Stop any current speech
        window.speechSynthesis.cancel()

        const utterance = new SpeechSynthesisUtterance(advisory.voice_advice)
        utterance.lang = 'hi-IN' // Support Hindi for Indian farmers
        utterance.onstart = () => setIsSpeaking(true)
        utterance.onend = () => setIsSpeaking(false)
        window.speechSynthesis.speak(utterance)
    }

    const getStageProgress = (s: string) => {
        switch (s) {
            case 'Seedling': return 20
            case 'Vegetative': return 40
            case 'Flowering': return 70
            case 'Harvest': return 100
            default: return 50
        }
    }

    return (
        <div className="flex-1 bg-[#f8fafc] min-h-screen p-4 md:p-8 space-y-8 max-w-7xl mx-auto pb-20">
            {/* 1. Header Section (Smart Context) */}
            <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 bg-white p-6 rounded-[32px] shadow-sm border border-gray-100">
                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-green-700 font-bold text-sm uppercase tracking-wider">
                        <MapPin className="h-4 w-4" />
                        {location ? `Lat: ${location.lat.toFixed(4)}, Lon: ${location.lon.toFixed(4)}` : "Detecting Location..."}
                    </div>
                    <h1 className="text-3xl font-black text-gray-900 leading-none">Smart Crop Advisory</h1>
                    <p className="text-gray-500 font-medium">Real-time agricultural insights tailored for your field</p>
                </div>

                <div className="flex flex-wrap gap-3 w-full lg:w-auto">
                    <div className="flex-1 lg:w-48">
                        <label className="text-[10px] font-bold text-gray-400 uppercase mb-1 block px-1">Current Crop</label>
                        <Select value={crop} onValueChange={setCrop}>
                            <SelectTrigger className="rounded-2xl h-12 bg-gray-50 border-none">
                                <SelectValue placeholder="Select Crop" />
                            </SelectTrigger>
                            <SelectContent className="rounded-2xl">
                                <SelectItem value="Tomato">Tomato</SelectItem>
                                <SelectItem value="Potato">Potato</SelectItem>
                                <SelectItem value="Wheat">Wheat</SelectItem>
                                <SelectItem value="Rice">Rice</SelectItem>
                                <SelectItem value="Grape">Grape</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="flex-1 lg:w-48">
                        <label className="text-[10px] font-bold text-gray-400 uppercase mb-1 block px-1">Crop Stage</label>
                        <Select value={stage} onValueChange={setStage}>
                            <SelectTrigger className="rounded-2xl h-12 bg-gray-50 border-none">
                                <SelectValue placeholder="Select Stage" />
                            </SelectTrigger>
                            <SelectContent className="rounded-2xl">
                                <SelectItem value="Seedling">Seedling</SelectItem>
                                <SelectItem value="Vegetative">Vegetative</SelectItem>
                                <SelectItem value="Flowering">Flowering</SelectItem>
                                <SelectItem value="Harvest">Harvest</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <Button
                        onClick={handleUpdate}
                        disabled={loading}
                        className="self-end h-12 rounded-2xl bg-green-700 hover:bg-green-800 px-6 shadow-lg shadow-green-700/20"
                    >
                        {loading ? "..." : "Update Advice"}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* 2. Weather-Based Advisory */}
                <Card className="rounded-[32px] border-none shadow-xl bg-white overflow-hidden group">
                    <CardHeader className="bg-blue-50/50 pb-4">
                        <div className="flex items-center justify-between">
                            <CardTitle className="text-lg flex items-center gap-2">
                                <Cloud className="h-5 w-5 text-blue-600" />
                                Weather Advice
                            </CardTitle>
                            <Badge className="bg-blue-100 text-blue-700 border-none">LIVE</Badge>
                        </div>
                    </CardHeader>
                    <CardContent className="pt-6 space-y-4">
                        <div className="flex items-center justify-between px-2">
                            <div className="flex items-center gap-3">
                                <div className="bg-blue-100 p-3 rounded-2xl">
                                    <Thermometer className="h-6 w-6 text-blue-700" />
                                </div>
                                <div>
                                    <div className="text-2xl font-black text-gray-900">{advisory?.weather.temp || '--'}°C</div>
                                    <div className="text-[10px] font-bold text-gray-400 uppercase">Temperature</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-3 text-right">
                                <div>
                                    <div className="text-2xl font-black text-gray-900">{advisory?.weather.humidity || '--'}%</div>
                                    <div className="text-[10px] font-bold text-gray-400 uppercase">Humidity</div>
                                </div>
                                <div className="bg-blue-100 p-3 rounded-2xl">
                                    <Droplets className="h-6 w-6 text-blue-700" />
                                </div>
                            </div>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-2xl border-l-4 border-blue-500">
                            <p className="text-sm font-bold text-gray-700 leading-snug">
                                {advisory?.weather.summary || "No weather data available."}
                            </p>
                            <ul className="mt-2 space-y-1">
                                {advisory?.weather.actionable_steps.map((step: string, i: number) => (
                                    <li key={i} className="text-xs text-blue-700 font-medium flex items-center gap-2">
                                        <div className="h-1 w-1 rounded-full bg-blue-400" />
                                        {step}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </CardContent>
                </Card>

                {/* 5. Disease Risk Prediction */}
                <Card className="rounded-[32px] border-none shadow-xl bg-white overflow-hidden">
                    <CardHeader className="bg-red-50/50 pb-4">
                        <CardTitle className="text-lg flex items-center gap-2">
                            <ShieldAlert className="h-5 w-5 text-red-600" />
                            Disease Risk AI
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 text-center space-y-6">
                        <div className="relative inline-block">
                            <div className={`h-24 w-24 rounded-full border-8 ${advisory?.disease_risk.level === 'High' ? 'border-red-500' :
                                advisory?.disease_risk.level === 'Medium' ? 'border-yellow-500' : 'border-green-500'
                                } flex items-center justify-center`}>
                                <div className="text-xl font-black">{advisory?.disease_risk.level || 'Low'}</div>
                            </div>
                            <div className="text-[10px] font-bold text-gray-400 uppercase mt-2">Current Risk Level</div>
                        </div>
                        <div className="bg-red-50 p-4 rounded-2xl space-y-1">
                            <p className="text-sm font-bold text-red-700 uppercase tracking-tight">AI PREDICTION</p>
                            <p className="text-xs font-medium text-gray-600">
                                {advisory?.disease_risk.reason || "Analyzing environmental factors..."}
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* 10. Voice Advisory (Farmer Friendly) */}
                <Card className="rounded-[32px] border-none shadow-xl bg-green-700 text-white overflow-hidden flex flex-col justify-between">
                    <CardHeader className="pb-0">
                        <CardTitle className="text-lg flex items-center gap-2 font-bold">
                            <Volume2 className="h-5 w-5" />
                            Voice Advisor
                        </CardTitle>
                        <CardDescription className="text-green-100 font-medium">Hindi/Local Audio Support</CardDescription>
                    </CardHeader>
                    <CardContent className="pb-8">
                        <div className="bg-white/10 p-4 rounded-2xl mb-6 backdrop-blur-sm min-h-[80px]">
                            <p className="text-sm italic font-medium leading-relaxed">
                                {advisory?.voice_advice || "Press play to hear your daily crop advice."}
                            </p>
                        </div>
                        <Button
                            onClick={speakAdvisory}
                            className={`w-full rounded-2xl h-14 font-black transition-all ${isSpeaking ? 'bg-white text-green-700 scale-95' : 'bg-white text-green-700 hover:bg-gray-100 shadow-xl'}`}
                        >
                            {isSpeaking ? (
                                <div className="flex items-center gap-3">
                                    <div className="flex gap-1">
                                        <div className="h-4 w-1 bg-green-700 animate-[bounce_1s_infinite]" />
                                        <div className="h-6 w-1 bg-green-700 animate-[bounce_1s_infinite_0.1s]" />
                                        <div className="h-4 w-1 bg-green-700 animate-[bounce_1s_infinite_0.2s]" />
                                    </div>
                                    NOW SPEAKING
                                </div>
                            ) : (
                                <>
                                    <Play className="h-5 w-5 mr-3 fill-current" />
                                    PLAY ADVISORY (HINDI)
                                </>
                            )}
                        </Button>
                    </CardContent>
                </Card>
            </div>

            {/* 4. Growth Stage Advisory (Smart Timeline) */}
            <Card className="rounded-[40px] border-none shadow-xl bg-white p-8">
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 mb-10">
                    <div>
                        <h2 className="text-2xl font-black text-gray-900 flex items-center gap-3">
                            <div className="h-8 w-2 bg-green-700 rounded-full"></div>
                            Crop Growth Smart Timeline
                        </h2>
                        <p className="text-gray-500 font-medium mt-1">Stage-wise optimized fertilizer and irrigation schedule</p>
                    </div>
                    <Badge className="bg-green-100 text-green-700 text-sm py-1.5 px-4 rounded-full font-bold">
                        {stage} Stage Active
                    </Badge>
                </div>

                <div className="space-y-12">
                    <div className="relative">
                        <Progress value={getStageProgress(stage)} className="h-4 rounded-full bg-gray-100" />
                        <div className="grid grid-cols-4 gap-4 mt-4">
                            {['Seedling', 'Vegetative', 'Flowering', 'Harvest'].map((s) => (
                                <div key={s} className="text-center space-y-1">
                                    <div className={`text-[10px] font-black uppercase tracking-tighter ${stage === s ? 'text-green-700' : 'text-gray-400'}`}>
                                        {s}
                                    </div>
                                    <div className={`h-2 w-2 rounded-full mx-auto ${stage === s ? 'bg-green-700 scale-125' : 'bg-gray-200'}`} />
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {[
                            { title: "Fertilizer Schedule", value: advisory?.growth_stage_timeline.fertilizer_schedule, icon: FlaskConical, color: "text-amber-600", bg: "bg-amber-50" },
                            { title: "Irrigation Schedule", value: advisory?.growth_stage_timeline.irrigation_schedule, icon: Droplets, color: "text-blue-600", bg: "bg-blue-50" },
                            { title: "Spray Schedule", value: advisory?.growth_stage_timeline.spray_schedule, icon: Wind, color: "text-purple-600", bg: "bg-purple-50" },
                        ].map((item, i) => (
                            <div key={i} className="flex gap-4 p-5 rounded-3xl bg-gray-50/50 hover:bg-white hover:shadow-lg transition-all border border-transparent hover:border-gray-100 select-none">
                                <div className={`${item.bg} p-4 rounded-2xl h-fit`}>
                                    <item.icon className={`h-6 w-6 ${item.color}`} />
                                </div>
                                <div className="space-y-1">
                                    <div className="text-xs font-black text-gray-400 uppercase tracking-widest">{item.title}</div>
                                    <p className="text-sm font-bold text-gray-700 leading-snug">{item.value || "Analyzing..."}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 3 & 6. Soil & Fertilizer Recommendation */}
                <Card className="rounded-[32px] border-none shadow-xl bg-white overflow-hidden">
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <FlaskConical className="h-5 w-5 text-amber-600" />
                            Soil-Based Recommendations
                        </CardTitle>
                        <CardDescription>Based on ICAR agricultural standards</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-3 gap-3">
                            {['N', 'P', 'K'].map(nut => (
                                <div key={nut} className="bg-gray-50 p-4 rounded-2xl text-center">
                                    <div className="text-lg font-black text-gray-900">--</div>
                                    <div className="text-[10px] font-bold text-gray-400">{nut} (ppm)</div>
                                </div>
                            ))}
                        </div>
                        <div className="p-5 rounded-[24px] bg-amber-50 border border-amber-100 space-y-3">
                            <div className="flex items-center gap-2 text-amber-700 text-xs font-black uppercase">
                                <Info className="h-3.5 w-3.5" />
                                Optimal Input Suggestion
                            </div>
                            <p className="text-sm font-bold text-gray-700">
                                {advisory?.soil_fertilizer.recommendation || "Upload soil report for precise NPK advice."}
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* 8. Government Scheme & Market Advisory */}
                <Card className="rounded-[32px] border-none shadow-xl bg-white overflow-hidden">
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <Landmark className="h-5 w-5 text-indigo-600" />
                            Market & Schemes
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-start gap-4 p-4 rounded-2xl bg-indigo-50 border border-indigo-100">
                            <div className="bg-indigo-100 p-2.5 rounded-xl">
                                <TrendingUp className="h-5 w-5 text-indigo-700" />
                            </div>
                            <div>
                                <div className="text-sm font-black text-indigo-900 uppercase tracking-tighter">Market Update</div>
                                <p className="text-xs font-medium text-gray-600">{advisory?.market_mandi.msp}</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-4 p-4 rounded-2xl bg-green-50 border border-green-100">
                            <div className="bg-green-100 p-2.5 rounded-xl">
                                <Landmark className="h-5 w-5 text-green-700" />
                            </div>
                            <div>
                                <div className="text-sm font-black text-green-900 uppercase tracking-tighter">Govt Subsidy</div>
                                <p className="text-xs font-medium text-gray-600">{advisory?.market_mandi.subsidy}</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* 9. Buy Recommended Products (Direct Links) */}
            <div className="space-y-4">
                <h2 className="text-xl font-black text-gray-900 flex items-center gap-2">
                    <ShoppingCart className="h-6 w-6 text-green-700" />
                    Recommended Products (E-commerce)
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[
                        { name: "Optimal NPK (19:19:19)", price: "₹450", platform: "Amazon", logo: "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg" },
                        { name: "Organic Neem Oil 1L", price: "₹280", platform: "Flipkart", logo: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Flipkart_logo.png" },
                        { name: "Fungicide Kavach", price: "₹620", platform: "BigHaat", logo: "https://www.bighaat.com/cdn/shop/files/BigHaat_Logo_Main_200x.png?v=1613567635" },
                        { name: "Smart Soil pH Meter", price: "₹1,200", platform: "Amazon", logo: "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg" },
                    ].map((prod, i) => (
                        <Card key={i} className="rounded-3xl border-none shadow-lg hover:shadow-2xl transition-all bg-white p-5 group">
                            <div className="h-10 w-10 bg-gray-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <img src={prod.logo} alt={prod.platform} className="h-6 w-6 object-contain" />
                            </div>
                            <h4 className="text-sm font-black text-gray-900 truncate">{prod.name}</h4>
                            <div className="flex items-center justify-between mt-4">
                                <div className="text-lg font-black text-green-700">{prod.price}</div>
                                <Button size="sm" variant="ghost" className="text-xs font-bold text-blue-600 hover:text-blue-700">BUY NOW</Button>
                            </div>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    )
}
