'use client'

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sprout, Calendar, MapPin, AlertTriangle, CheckCircle, Droplets, Wind, Thermometer, History, TrendingUp } from "lucide-react"

interface CropDetail {
    id: string
    name: string
    variety?: string
    planting_date?: string
    expected_harvest_date?: string
    status: string
    area_size?: number
    area_unit?: string
    location_name?: string
    image_url?: string
}

export default function CropDetailPage() {
    const params = useParams()
    const [crop, setCrop] = useState<CropDetail | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchCropDetails()
    }, [])

    const fetchCropDetails = async () => {
        try {
            const token = localStorage.getItem("token")
            const res = await fetch(`http://localhost:8000/api/v1/crops/${params.id}`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setCrop(data)
            }
        } catch (error) {
            console.error("Error fetching crop details:", error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <div className="p-8 text-center">Loading dashboard...</div>
    if (!crop) return <div className="p-8 text-center">Crop not found</div>

    const daysSinceSowing = crop.planting_date
        ? Math.floor((new Date().getTime() - new Date(crop.planting_date).getTime()) / (1000 * 3600 * 24))
        : 0

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 space-y-8 max-w-7xl mx-auto">
            {/* Header / Overview Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex items-center gap-4">
                    <div className="h-16 w-16 bg-green-100 rounded-xl flex items-center justify-center text-green-700">
                        <Sprout className="h-8 w-8" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">{crop.name}</h1>
                        <div className="flex items-center gap-3 text-sm text-gray-500 mt-1">
                            <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {crop.location_name || "Farm Location"}</span>
                            <span>•</span>
                            <span>{crop.area_size} {crop.area_unit}</span>
                            <span>•</span>
                            <span>{crop.variety || "Local Variety"}</span>
                        </div>
                    </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                    <Badge className={`px-3 py-1 text-sm ${crop.status === 'HEALTHY' ? 'bg-green-100 text-green-700 border-green-200' : 'bg-red-100 text-red-700 border-red-200'}`}>
                        {crop.status === 'HEALTHY' ? 'Healthy Crop' : 'Attention Needed'}
                    </Badge>
                    <span className="text-xs text-gray-400">Last updated: Today</span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Status & Timeline */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Disease Status Section */}
                    {crop.status !== 'HEALTHY' && (
                        <Card className="border-l-4 border-l-red-500 shadow-md">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-red-600">
                                    <AlertTriangle className="h-5 w-5" />
                                    Active Disease Alert: Late Blight
                                </CardTitle>
                                <CardDescription>Detected on {new Date().toLocaleDateString()} with 92% confidence.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="bg-red-50 p-4 rounded-lg text-sm text-red-800 mb-4">
                                    <strong>Severity: High.</strong> Immediate action recommended to prevent spread.
                                </div>
                                <Button className="w-full bg-red-600 hover:bg-red-700">View Treatment & Spray Guide</Button>
                            </CardContent>
                        </Card>
                    )}

                    {/* Growth Tracker */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <TrendingUp className="h-5 w-5 text-green-600" />
                                Growth Progress
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div className="flex justify-between text-sm font-medium">
                                    <span>Day {daysSinceSowing}</span>
                                    <span>Est. Harvest: {crop.expected_harvest_date || "N/A"}</span>
                                </div>
                                <div className="h-3 w-full bg-gray-100 rounded-full overflow-hidden">
                                    <div className="h-full bg-green-500 w-[45%] rounded-full"></div>
                                </div>
                                <div className="flex justify-between text-xs text-gray-400">
                                    <span>Sowing</span>
                                    <span className="text-green-600 font-bold">Vegetative Stage</span>
                                    <span>Harvest</span>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* History Timeline */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <History className="h-5 w-5 text-purple-600" />
                                Scan History
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6 border-l-2 border-gray-100 pl-6 ml-2">
                                <div className="relative">
                                    <div className="absolute -left-[31px] top-1 h-4 w-4 rounded-full bg-green-500 border-2 border-white"></div>
                                    <div className="text-sm font-bold text-gray-900">Health Check - Clear</div>
                                    <div className="text-xs text-gray-500">2 days ago</div>
                                    <p className="text-sm text-gray-600 mt-1">Leaf scan showed no signs of disease.</p>
                                </div>
                                <div className="relative">
                                    <div className="absolute -left-[31px] top-1 h-4 w-4 rounded-full bg-gray-300 border-2 border-white"></div>
                                    <div className="text-sm font-bold text-gray-900">Crop Added</div>
                                    <div className="text-xs text-gray-500">{crop.planting_date}</div>
                                    <p className="text-sm text-gray-600 mt-1">Initial registration of crop.</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Right Column: Weather & Actions */}
                <div className="space-y-8">

                    {/* Weather Risk Panel */}
                    <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-none shadow-sm">
                        <CardHeader>
                            <CardTitle className="text-blue-800 flex items-center gap-2">
                                <Wind className="h-5 w-5" />
                                Weather Risk
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-2 gap-4 mb-4">
                                <div className="bg-white/60 p-3 rounded-lg flex flex-col items-center">
                                    <Thermometer className="h-6 w-6 text-orange-500 mb-1" />
                                    <span className="font-bold text-gray-800">28°C</span>
                                    <span className="text-xs text-gray-500">Temp</span>
                                </div>
                                <div className="bg-white/60 p-3 rounded-lg flex flex-col items-center">
                                    <Droplets className="h-6 w-6 text-blue-500 mb-1" />
                                    <span className="font-bold text-gray-800">72%</span>
                                    <span className="text-xs text-gray-500">Humidity</span>
                                </div>
                            </div>
                            <div className="bg-yellow-100 text-yellow-800 p-3 rounded-lg text-xs border border-yellow-200">
                                <strong>Moderate Fungal Risk:</strong> High humidity forecast for next 3 days. Monitor leaves closely.
                            </div>
                        </CardContent>
                    </Card>

                    {/* Recommended Actions */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <CheckCircle className="h-5 w-5 text-green-600" />
                                Recommended Actions
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                                    <input type="checkbox" className="mt-1 h-4 w-4 text-green-600 rounded" />
                                    <div className="text-sm">
                                        <p className="font-medium text-gray-900">Weekly Shield Spray</p>
                                        <p className="text-xs text-gray-500">Preventative neem oil spray.</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                                    <input type="checkbox" className="mt-1 h-4 w-4 text-green-600 rounded" />
                                    <div className="text-sm">
                                        <p className="font-medium text-gray-900">Check Soil Moisture</p>
                                        <p className="text-xs text-gray-500">Ensure active root growth.</p>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                </div>
            </div>
        </div>
    )
}
