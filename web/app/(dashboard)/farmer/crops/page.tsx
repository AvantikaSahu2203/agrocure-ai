'use client'

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Plus, Sprout, Calendar, MapPin } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import api from "@/lib/api"

interface Crop {
    id: string
    name: string
    variety?: string
    planting_date?: string
    status: string
    image_url?: string
    location_name?: string
}

export default function CropsPage() {
    const [crops, setCrops] = useState<Crop[]>([])
    const [loading, setLoading] = useState(true)
    const router = useRouter()

    useEffect(() => {
        fetchCrops()
    }, [])

    const fetchCrops = async () => {
        try {
            const res = await api.get("/crops/")
            setCrops(res.data)
        } catch (error) {
            console.error("Failed to fetch crops", error)
        } finally {
            setLoading(false)
        }
    }

    const calculateDays = (dateString?: string) => {
        if (!dateString) return 0
        const start = new Date(dateString)
        const now = new Date()
        const diff = now.getTime() - start.getTime()
        return Math.floor(diff / (1000 * 3600 * 24))
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 border-l-4 border-green-600 pl-3">My Crops</h1>
                    <p className="text-gray-500 text-sm pl-4 mt-1">Manage and track your farm's produce</p>
                </div>
                <Link href="/farmer/crops/add">
                    <Button className="bg-green-600 hover:bg-green-700">
                        <Plus className="h-5 w-5 mr-2" />
                        Add New Crop
                    </Button>
                </Link>
            </div>

            {/* Crops Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="col-span-full py-20 text-center text-gray-500">Loading crops...</div>
                ) : crops.length > 0 ? (
                    crops.map((crop) => (
                        <Link href={`/farmer/crops/${crop.id}`} key={crop.id}>
                            <Card className="hover:shadow-md transition-shadow cursor-pointer overflow-hidden group">
                                <div className="h-40 bg-green-50 relative">
                                    {crop.image_url ? (
                                        <img src={crop.image_url} alt={crop.name} className="w-full h-full object-cover" />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center text-green-200">
                                            <Sprout className="h-16 w-16" />
                                        </div>
                                    )}
                                    <div className="absolute top-3 right-3">
                                        <Badge variant={crop.status === 'HEALTHY' ? 'default' : 'destructive'}>
                                            {crop.status}
                                        </Badge>
                                    </div>
                                </div>
                                <CardContent className="p-5">
                                    <h3 className="font-bold text-lg text-gray-900 group-hover:text-green-700 transition-colors">
                                        {crop.name}
                                    </h3>
                                    <p className="text-sm text-gray-500 mb-4">{crop.variety || "Unknown Variety"}</p>

                                    <div className="space-y-2 text-sm text-gray-600">
                                        <div className="flex items-center gap-2">
                                            <Calendar className="h-4 w-4 text-gray-400" />
                                            <span>{calculateDays(crop.planting_date)} days since sowing</span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <MapPin className="h-4 w-4 text-gray-400" />
                                            <span>{crop.location_name || "Main Field"}</span>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center bg-white rounded-xl border border-dashed border-gray-300">
                        <Sprout className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                        <h3 className="font-medium text-gray-900">No crops added yet</h3>
                        <p className="text-gray-500 text-sm mb-4">Start by adding your first crop to track its health.</p>
                        <Link href="/farmer/crops/add">
                            <Button variant="outline">Add Crop</Button>
                        </Link>
                    </div>
                )}
            </div>
        </div>
    )
}
