'use client'

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Sprout, Wheat, Leaf, Search, Grape, Info } from "lucide-react"

import api from "@/lib/api"

// Define a type for the disease based on the API response
interface Disease {
    name: string
    scientific_name: string
    symptoms: string[]
    recommendations: string[]
    crop_name: string
    chemical_treatment?: string
    organic_treatment?: string
}

export default function DiseaseLibraryPage() {
    const [diseases, setDiseases] = useState<Disease[]>([])
    const [searchTerm, setSearchTerm] = useState("")
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchDiseases() {
            try {
                const res = await api.get("/diseases")
                setDiseases(res.data)
            } catch (error) {
                console.error("Failed to fetch diseases", error)
            } finally {
                setLoading(false)
            }
        }
        fetchDiseases()
    }, [])

    const filteredDiseases = diseases.filter(disease =>
        disease.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        disease.crop_name.toLowerCase().includes(searchTerm.toLowerCase())
    )

    const getCropIcon = (cropName: string) => {
        switch (cropName.toLowerCase()) {
            case 'tomato': return <div className="bg-red-100 p-3 rounded-xl"><div className="h-6 w-6 rounded-full bg-red-500/20 flex items-center justify-center"><div className="h-4 w-4 rounded-full bg-red-500"></div></div></div>
            case 'potato': return <div className="bg-amber-100 p-3 rounded-xl"><div className="h-6 w-6 rounded-full bg-amber-500/20 flex items-center justify-center"><div className="h-4 w-4 rounded-full bg-amber-600"></div></div></div>
            case 'wheat': return <div className="bg-yellow-100 p-3 rounded-xl"><Wheat className="h-6 w-6 text-yellow-600" /></div>
            case 'rice': return <div className="bg-green-100 p-3 rounded-xl"><Sprout className="h-6 w-6 text-green-600" /></div>
            case 'grape': return <div className="bg-purple-100 p-3 rounded-xl"><Grape className="h-6 w-6 text-purple-600" /></div>
            default: return <div className="bg-green-50 p-3 rounded-xl"><Leaf className="h-6 w-6 text-green-500" /></div>
        }
    }

    // Mock Severity for UI demo (since existing DB doesn't have explicit severity field for *general* description, 
    // only calculates it per image analysis. We'll randomise or hardcode for the library view as "Risk Level")
    const getRiskTag = (index: number) => {
        if (index % 3 === 0) return <span className="bg-red-100 text-red-600 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wide">High</span>
        if (index % 3 === 1) return <span className="bg-yellow-100 text-yellow-600 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wide">Medium</span>
        return <span className="bg-blue-100 text-blue-600 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wide">Low</span>
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 space-y-6 max-w-5xl mx-auto">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-900 border-l-4 border-green-700 pl-3">Disease Library</h1>
            </div>

            <div className="relative">
                <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <Input
                    className="pl-10 h-12 rounded-xl border-gray-200 bg-white shadow-sm"
                    placeholder="Search diseases..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            <div className="space-y-4">
                {loading ? (
                    <div className="text-center py-10 text-gray-500">Loading library...</div>
                ) : filteredDiseases.length > 0 ? (
                    filteredDiseases.map((disease, index) => (
                        <Card key={index} className="rounded-2xl border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer bg-white group">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    {getCropIcon(disease.crop_name)}
                                    <div>
                                        <h4 className="font-bold text-gray-900 text-lg group-hover:text-green-700 transition-colors">{disease.name}</h4>
                                        <p className="text-gray-500 text-sm">{disease.crop_name}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    {getRiskTag(index)}
                                </div>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <div className="text-center py-10 text-gray-500 flex flex-col items-center">
                        <Info className="h-10 w-10 text-gray-300 mb-2" />
                        <p>No diseases found.</p>
                    </div>
                )}
            </div>
        </div>
    )
}
