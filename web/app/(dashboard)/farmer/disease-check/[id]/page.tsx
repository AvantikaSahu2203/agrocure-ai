'use client'

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
    AlertTriangle,
    CheckCircle,
    ArrowLeft,
    Thermometer,
    Droplets,
    FlaskConical,
    ShieldCheck,
    MapPin,
    PhoneCall,
    Volume2,
    VolumeX,
    ShoppingCart,
    Info,
    ExternalLink
} from "lucide-react"
import Image from "next/image"
import api from "@/lib/api"

export default function DiseaseDetailPage() {
    const { id } = useParams()
    const router = useRouter()
    const [report, setReport] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [isSpeaking, setIsSpeaking] = useState(false)

    useEffect(() => {
        async function fetchReport() {
            try {
                const res = await api.get(`/reports/${id}`)
                setReport(res.data)
            } catch (err: any) {
                setError(err.response?.data?.detail || err.message)
            } finally {
                setLoading(false)
            }
        }
        fetchReport()
    }, [id])

    const handleVoiceAdvisory = () => {
        if (!report) return

        if (isSpeaking) {
            window.speechSynthesis.cancel()
            setIsSpeaking(false)
            return
        }

        const analysis = report.details?.analysis || {}
        const textToSpeak = `
            Disease Detected: ${report.detected_disease}. 
            Severity is ${analysis.severity}. 
            Symptoms include: ${analysis.symptoms_detected?.join(", ") || "various leaf spots"}.
            Organic Solution: ${analysis.organic_treatment}. 
            Chemical Solution: ${analysis.chemical_treatment}.
            Keep following the prevention tips for better crop health.
        `

        const utterance = new SpeechSynthesisUtterance(textToSpeak)
        utterance.lang = 'hi-IN' // Attempting Hindi for better accessibility
        utterance.onend = () => setIsSpeaking(false)

        setIsSpeaking(true)
        window.speechSynthesis.speak(utterance)
    }

    if (loading) return (
        <div className="flex-1 flex items-center justify-center min-h-screen bg-gray-50">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-700"></div>
        </div>
    )

    if (error || !report) return (
        <div className="flex-1 p-8 bg-gray-50 min-h-screen">
            <Card className="max-w-md mx-auto mt-10">
                <CardContent className="pt-6 text-center">
                    <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                    <h2 className="text-xl font-bold mb-2">Error Loading Report</h2>
                    <p className="text-gray-500 mb-6">{error || "Report not found"}</p>
                    <Button onClick={() => router.back()} className="w-full bg-green-700">Go Back</Button>
                </CardContent>
            </Card>
        </div>
    )

    const analysis = report.details?.analysis || {}
    const cropInfo = analysis.crop_info || { name: "Unknown Crop" }

    // Fallback logic for different schemas (Seeded vs Orchestrator)
    const symptoms = analysis.symptoms_detected || analysis.symptoms || []
    const recommendations = analysis.recommendations || analysis.preventative_measures || []
    const organicTreatment = analysis.organic_treatment || analysis.organic_remedy
    const chemicalTreatment = analysis.chemical_treatment || analysis.chemical_remedy
    const getImageUrl = (url: string) => {
        if (!url) return "https://images.unsplash.com/photo-1628102422220-23cfc4c1a71e?q=80&w=2000"
        if (url.startsWith('http')) return url
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
        const base = baseUrl.replace('/api/v1', '')
        return `${base.endsWith('/') ? base.slice(0, -1) : base}/${url.startsWith('/') ? url.slice(1) : url}`
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen pb-20 p-4 md:p-8 max-w-5xl mx-auto space-y-6">
            {/* Navigation */}
            <Button variant="ghost" onClick={() => router.back()} className="mb-2 text-gray-600 hover:text-green-700">
                <ArrowLeft className="mr-2 h-4 w-4" /> Back to Dashboard
            </Button>

            {/* 1. Disease Header Section */}
            <div className="relative rounded-[32px] overflow-hidden shadow-2xl bg-white border border-gray-100">
                <div className="relative h-64 md:h-80 w-full">
                    <Image
                        src={getImageUrl(report.image_url)}
                        alt={report.detected_disease}
                        fill
                        className="object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                    <div className="absolute bottom-0 left-0 p-6 md:p-10 w-full flex flex-col md:flex-row md:items-end justify-between gap-4">
                        <div className="space-y-2">
                            <Badge className="bg-green-600 hover:bg-green-700 text-white border-none px-3 py-1 rounded-full uppercase text-[10px] font-bold tracking-widest">
                                {cropInfo.name}
                            </Badge>
                            <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight">
                                {report.detected_disease}
                            </h1>
                            <p className="text-green-200 font-medium italic text-sm md:text-lg">
                                {analysis.scientific_name || "Diagnostic Result"}
                            </p>
                        </div>
                        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/20 text-center min-w-[120px]">
                            <div className="text-3xl font-black text-white">{(report.confidence_score * 100).toFixed(0)}%</div>
                            <div className="text-[10px] font-bold text-green-300 uppercase tracking-widest">Confidence</div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Column: Details */}
                <div className="md:col-span-2 space-y-6">

                    {/* 2. Symptoms Section */}
                    {symptoms.length > 0 && (
                        <Card className="rounded-[24px] border-none shadow-lg">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-gray-900">
                                    <Info className="h-5 w-5 text-indigo-600" />
                                    Visual Symptoms
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                {symptoms.map((symptom: string, i: number) => (
                                    <div key={i} className="flex items-center gap-3 p-3 bg-indigo-50/50 rounded-xl border border-indigo-100">
                                        <div className="h-2 w-2 rounded-full bg-indigo-500" />
                                        <span className="text-sm font-medium text-indigo-900">{symptom}</span>
                                    </div>
                                ))}
                            </CardContent>
                        </Card>
                    )}

                    {/* 3. Causes Section (ICAR Reference) */}
                    <Card className="rounded-[24px] border-none shadow-lg overflow-hidden">
                        <div className="bg-amber-500 h-1 w-full" />
                        <CardHeader>
                            <CardTitle className="text-amber-900">Primary Causes & Etiology</CardTitle>
                            <CardDescription>Based on ICAR Agricultural Standards</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-gray-700 leading-relaxed italic bg-amber-50/30 p-4 rounded-2xl border border-amber-100">
                                "{analysis.analysis || analysis.description || "The disease is primarily caused by environmental factors and pathogens specific to this crop variety. It thrives in conditions observed in your recent weather context."}"
                            </p>
                        </CardContent>
                    </Card>

                    {/* 5. Treatment & Cure Section */}
                    <Card className="rounded-[24px] border-none shadow-lg">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <FlaskConical className="h-5 w-5 text-blue-600" />
                                Treatment & Recovery Plan
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div className="p-4 bg-green-50 rounded-2xl border border-green-100">
                                    <h4 className="text-xs font-black text-green-800 uppercase tracking-widest mb-2">Organic Method</h4>
                                    <p className="text-sm font-medium text-gray-800">{organicTreatment || "Apply Neem Oil spray (5ml/L) and remove infected leaves manually."}</p>
                                </div>
                                <div className="p-4 bg-blue-50 rounded-2xl border border-blue-100">
                                    <h4 className="text-xs font-black text-blue-800 uppercase tracking-widest mb-2">Chemical Method</h4>
                                    <p className="text-sm font-medium text-gray-800">{chemicalTreatment || "Spray Metalaxyl or Mancozeb based fungicide at 2g per liter."}</p>
                                </div>
                            </div>
                            <div className="p-4 bg-gray-50 rounded-2xl border border-gray-100">
                                <h4 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Application Frequency</h4>
                                <p className="text-sm font-bold text-gray-800">{analysis.dosage || "Consult your local agri-expert for precise application schedule."}</p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* 6. Recommended Medicines Section */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-black text-gray-800 flex items-center gap-2 ml-2">
                            <ShoppingCart className="h-5 w-5 text-purple-600" />
                            Recommended Products
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <Card className="rounded-2xl border border-purple-100 hover:shadow-md transition-all cursor-pointer group">
                                <CardContent className="p-4 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="h-12 w-12 bg-purple-100 rounded-xl flex items-center justify-center group-hover:bg-purple-600 transition-colors">
                                            <ShoppingCart className="h-6 w-6 text-purple-600 group-hover:text-white" />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-gray-900">Standard Fungicide</h4>
                                            <p className="text-xs text-gray-500">Mancozeb 75% WP</p>
                                        </div>
                                    </div>
                                    <a href="https://www.amazon.in/s?k=fungicide+for+plants" target="_blank" className="p-2 bg-gray-50 rounded-lg hover:bg-purple-50">
                                        <ExternalLink className="h-4 w-4 text-purple-600" />
                                    </a>
                                </CardContent>
                            </Card>
                            <Card className="rounded-2xl border border-purple-100 hover:shadow-md transition-all cursor-pointer group">
                                <CardContent className="p-4 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="h-12 w-12 bg-purple-100 rounded-xl flex items-center justify-center group-hover:bg-purple-600 transition-colors">
                                            <ShoppingCart className="h-6 w-6 text-purple-600 group-hover:text-white" />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-gray-900">Organic Remedy</h4>
                                            <p className="text-xs text-gray-500">Pure Neem Oil (Cold Pressed)</p>
                                        </div>
                                    </div>
                                    <a href="https://www.amazon.in/s?k=neem+oil+for+plants" target="_blank" className="p-2 bg-gray-50 rounded-lg hover:bg-purple-50">
                                        <ExternalLink className="h-4 w-4 text-purple-600" />
                                    </a>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>

                {/* Right Column: Alerts & Expert */}
                <div className="space-y-6">

                    {/* 4. Spread Conditions Section */}
                    <Card className="rounded-[24px] border-none shadow-lg bg-gradient-to-br from-orange-500 to-red-600 text-white p-1">
                        <CardContent className="p-6 space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="font-bold text-lg">Spread Risk</h3>
                                <AlertTriangle className="h-5 w-5 text-white/80" />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-3 bg-white/10 rounded-2xl border border-white/20">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Thermometer className="h-3 w-3" />
                                        <span className="text-[10px] font-bold uppercase opacity-80">Ideal Temp</span>
                                    </div>
                                    <div className="text-lg font-black">20-28°C</div>
                                </div>
                                <div className="p-3 bg-white/10 rounded-2xl border border-white/20">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Droplets className="h-3 w-3" />
                                        <span className="text-[10px] font-bold uppercase opacity-80">Humidity</span>
                                    </div>
                                    <div className="text-lg font-black">{">"}85%</div>
                                </div>
                            </div>
                            <p className="text-xs font-medium text-white/90 leading-relaxed border-t border-white/10 pt-4">
                                Current high humidity in your region significantly increases spore germination. Preventive spray is highly recommended.
                            </p>
                        </CardContent>
                    </Card>

                    {/* 7. Prevention Tips Section */}
                    {recommendations.length > 0 && (
                        <Card className="rounded-[24px] border-none shadow-lg">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <ShieldCheck className="h-5 w-5 text-green-600" />
                                    Prevention Tips
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <ul className="space-y-3">
                                    {recommendations.map((rec: string, i: number) => (
                                        <li key={i} className="flex gap-3 text-sm font-medium text-gray-700">
                                            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
                                            {rec}
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    )}

                    {/* 8. Nearby Agro Shops Section */}
                    <Card className="rounded-[24px] border-none shadow-lg bg-gray-900 text-white overflow-hidden">
                        <div className="h-32 w-full bg-gray-800 relative group cursor-pointer overflow-hidden">
                            <MapPin className="h-10 w-10 text-white/20 absolute inset-0 m-auto group-hover:scale-110 transition-transform" />
                            <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-gray-900 to-transparent">
                                <p className="text-xs font-bold text-green-400">View Nearby Shops</p>
                            </div>
                        </div>
                        <CardContent className="p-5 space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="font-bold text-sm">Pune Agri Center</span>
                                <Badge className="bg-green-700 text-[10px]">2 km</Badge>
                            </div>
                            <Button className="w-full bg-green-700 hover:bg-green-800 rounded-xl h-10 font-bold text-xs uppercase tracking-wider">
                                <MapPin className="h-3.5 w-3.5 mr-2" />
                                Get Directions
                            </Button>
                        </CardContent>
                    </Card>

                    {/* 9. Expert Help / Voice Guide Section */}
                    <div className="grid grid-cols-2 gap-3">
                        <Button
                            onClick={handleVoiceAdvisory}
                            className={`rounded-2xl h-14 flex flex-col items-center justify-center ${isSpeaking ? 'bg-indigo-700' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                        >
                            {isSpeaking ? <VolumeX className="h-5 w-5 mb-1" /> : <Volume2 className="h-5 w-5 mb-1" />}
                            <span className="text-[10px] font-bold uppercase tracking-wider">Voice Guide</span>
                        </Button>
                        <Button className="rounded-2xl h-14 flex flex-col items-center justify-center bg-teal-600 hover:bg-teal-700">
                            <PhoneCall className="h-5 w-5 mb-1" />
                            <span className="text-[10px] font-bold uppercase tracking-wider">Call Expert</span>
                        </Button>
                    </div>

                </div>
            </div>
        </div>
    )
}
