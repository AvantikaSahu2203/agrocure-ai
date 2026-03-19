'use client'

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { ArrowLeft, Loader2 } from "lucide-react"
import Link from "next/link"
import api from "@/lib/api"

export default function AddCropPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
        name: "",
        variety: "",
        planting_date: "",
        expected_harvest_date: "",
        area_size: "",
        area_unit: "Acres",
        location_name: ""
    })

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        try {
            const response = await api.post("/crops/", {
                ...formData,
                area_size: parseFloat(formData.area_size) || 0
            })

            if (response.status === 200 || response.status === 201) {
                router.push("/farmer/crops")
            } else {
                console.error("Failed to create crop")
            }
        } catch (error) {
            console.error("Error creating crop:", error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 flex items-center justify-center">
            <Card className="w-full max-w-2xl shadow-lg border-none">
                <CardHeader>
                    <div className="flex items-center gap-4 mb-2">
                        <Link href="/farmer/crops">
                            <Button variant="ghost" size="sm" className="p-0 h-auto">
                                <ArrowLeft className="h-5 w-5 text-gray-500" />
                            </Button>
                        </Link>
                        <CardTitle className="text-2xl font-bold text-gray-900">Add New Crop</CardTitle>
                    </div>
                    <CardDescription>Enter details about your crop to start tracking its health.</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <Label htmlFor="name">Crop Name</Label>
                                <Input
                                    id="name"
                                    name="name"
                                    placeholder="e.g. Tomato - Field 1"
                                    required
                                    value={formData.name}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="variety">Variety</Label>
                                <Input
                                    id="variety"
                                    name="variety"
                                    placeholder="e.g. Hybrid 455"
                                    value={formData.variety}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="planting_date">Planting Date</Label>
                                <Input
                                    id="planting_date"
                                    name="planting_date"
                                    type="date"
                                    required
                                    value={formData.planting_date}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="expected_harvest_date">Expected Harvest</Label>
                                <Input
                                    id="expected_harvest_date"
                                    name="expected_harvest_date"
                                    type="date"
                                    value={formData.expected_harvest_date}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="area_size">Field Size</Label>
                                <div className="flex gap-2">
                                    <Input
                                        id="area_size"
                                        name="area_size"
                                        type="number"
                                        step="0.1"
                                        placeholder="2.5"
                                        value={formData.area_size}
                                        onChange={handleChange}
                                    />
                                    <select
                                        name="area_unit"
                                        value={formData.area_unit}
                                        onChange={handleChange}
                                        className="border rounded-md px-3 text-sm bg-white"
                                    >
                                        <option value="Acres">Acres</option>
                                        <option value="Hectares">Hectares</option>
                                        <option value="Guntha">Guntha</option>
                                    </select>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="location_name">Location / Village</Label>
                                <Input
                                    id="location_name"
                                    name="location_name"
                                    placeholder="e.g. North Farm, Pune"
                                    value={formData.location_name}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div className="pt-4 flex justify-end gap-3">
                            <Link href="/farmer/crops">
                                <Button variant="outline" type="button">Cancel</Button>
                            </Link>
                            <Button type="submit" className="bg-green-600 hover:bg-green-700 w-32" disabled={loading}>
                                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Save Crop"}
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
