'use client'

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload, Loader2, AlertTriangle, CheckCircle, Droplets, FlaskConical, Sprout } from "lucide-react"
import Image from "next/image"
import api from "@/lib/api"

export default function DiseaseCheckPage() {
    const router = useRouter()
    const [selectedImage, setSelectedImage] = useState<File | null>(null)
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [cropName, setCropName] = useState("Tomato")
    const [region, setRegion] = useState("Pune")
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<any>(null)
    const [error, setError] = useState<string | null>(null)

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0]
            setSelectedImage(file)
            setPreviewUrl(URL.createObjectURL(file))
            setResult(null)
            setError(null)
        }
    }

    const handleAnalyze = async () => {
        if (!selectedImage) return

        setLoading(true)
        setError(null)

        const formData = new FormData()
        formData.append("image", selectedImage)
        formData.append("crop_name", cropName)
        formData.append("city", region)
        formData.append("state", "Maharashtra")
        formData.append("lat", "18.5204")
        formData.append("lon", "73.8567")

        try {
            const response = await api.post("/orchestrator/full-analysis", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })

            const data = response.data
            setResult(data)

            // Redirect to detail page if report ID is present
            if (data.report_id) {
                router.push(`/farmer/disease-check/${data.report_id}`)
            }
        } catch (err: any) {
            console.error(err)
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex-1 space-y-4 p-8 pt-6">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold text-green-800">Crop Disease Diagnosis</h2>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                {/* Upload Section */}
                <div className="space-y-4">
                    <Card className="border-green-100">
                        <CardHeader>
                            <CardTitle>Disease Analysis</CardTitle>
                            <CardDescription>Upload a leaf photo and specify the crop for accurate diagnosis.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="cropName">Crop Name</Label>
                                <Input
                                    id="cropName"
                                    value={cropName}
                                    onChange={(e) => setCropName(e.target.value)}
                                    placeholder="e.g. Tomato, Mango, Rice"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="region">City/Region</Label>
                                <Input
                                    id="region"
                                    value={region}
                                    onChange={(e) => setRegion(e.target.value)}
                                    placeholder="e.g. Pune, Nagpur"
                                />
                            </div>

                            <div className="grid w-full items-center gap-1.5">
                                <Label htmlFor="picture">Plant Image</Label>
                                <Input id="picture" type="file" accept="image/*" onChange={handleImageChange} className="cursor-pointer" />
                            </div>

                            <div className="flex gap-2">
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={async () => {
                                        const res = await fetch('/sample-leaf.jpg');
                                        const blob = await res.blob();
                                        const file = new File([blob], "sample-leaf.jpg", { type: "image/jpeg" });
                                        setSelectedImage(file);
                                        setPreviewUrl(URL.createObjectURL(file));
                                    }}
                                    className="flex-1 text-xs border-green-200 text-green-700 hover:bg-green-50"
                                >
                                    <Upload className="h-3 w-3 mr-1" /> Use Sample Image
                                </Button>
                            </div>

                            {previewUrl && (
                                <div className="relative aspect-video w-full overflow-hidden rounded-xl border border-green-50 shadow-sm">
                                    <Image
                                        src={previewUrl}
                                        alt="Preview"
                                        fill
                                        className="object-cover"
                                    />
                                </div>
                            )}

                            <Button
                                onClick={handleAnalyze}
                                disabled={!selectedImage || loading || !cropName}
                                className="w-full bg-green-600 hover:bg-green-700 h-12 text-lg"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                        Analyzing Plant...
                                    </>
                                ) : (
                                    <>
                                        <Sprout className="mr-2 h-5 w-5" />
                                        Run Full Diagnostic
                                    </>
                                )}
                            </Button>
                            {error && <p className="text-red-500 text-sm font-medium text-center bg-red-50 p-2 rounded">{error}</p>}
                        </CardContent>
                    </Card>

                    {/* Store Link Section (Moved here for better layout) */}
                    {result && (
                        <Card className="border-green-200 bg-green-50/30">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-green-800 text-lg">Acquire Treatment Online</CardTitle>
                            </CardHeader>
                            <CardContent className="flex gap-2">
                                <a
                                    href={result.ecommerce_links.amazon_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex-1 text-center px-4 py-2 bg-white border border-green-200 rounded-md hover:bg-green-50 text-green-800 font-medium transition-colors shadow-sm"
                                >
                                    Amazon
                                </a>
                                <a
                                    href={result.ecommerce_links.flipkart_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex-1 text-center px-4 py-2 bg-white border border-green-200 rounded-md hover:bg-green-50 text-green-800 font-medium transition-colors shadow-sm"
                                >
                                    Flipkart
                                </a>
                                <a
                                    href={result.ecommerce_links.google_search_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex-1 text-center px-4 py-2 bg-white border border-green-200 rounded-md hover:bg-green-50 text-green-800 font-medium transition-colors shadow-sm"
                                >
                                    Nearby Stores
                                </a>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Results Section */}
                <div className="space-y-4">
                    {!result && !loading && (
                        <div className="h-full flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-gray-200 rounded-xl bg-gray-50/50">
                            <CheckCircle className="h-12 w-12 text-gray-300 mb-4" />
                            <p className="text-gray-500">Analysis results will appear here after scanning.</p>
                        </div>
                    )}

                    {loading && (
                        <div className="h-full flex flex-col items-center justify-center p-12 space-y-4">
                            <Loader2 className="h-12 w-12 text-green-600 animate-spin" />
                            <p className="text-green-700 font-medium">Processing leaf imagery and environmental context...</p>
                        </div>
                    )}

                    {result && (
                        <>
                            {/* Disease Identity Card */}
                            <Card className="border-red-200 bg-red-50 shadow-sm overflow-hidden">
                                <div className="h-1 bg-red-500 w-full" />
                                <CardHeader>
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <CardTitle className="flex items-center text-red-800 text-2xl font-bold">
                                                <AlertTriangle className="mr-2 h-6 w-6 text-red-600" />
                                                {result.disease_analysis.disease_name}
                                            </CardTitle>
                                            <p className="text-red-600/80 font-medium italic mt-1">
                                                {result.disease_analysis.scientific_name}
                                            </p>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-2xl font-black text-red-700">
                                                {(result.disease_analysis.confidence * 100).toFixed(0)}%
                                            </div>
                                            <div className="text-xs font-bold text-red-600 tracking-wider">CONFIDENCE</div>
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="flex gap-4">
                                        <div className="flex-1 bg-white/50 p-3 rounded-lg border border-red-100">
                                            <span className="text-xs font-bold text-red-800 block mb-1">SEVERITY</span>
                                            <span className="font-bold text-red-700">{result.disease_analysis.severity?.toUpperCase()}</span>
                                        </div>
                                        <div className="flex-1 bg-white/50 p-3 rounded-lg border border-red-100">
                                            <span className="text-xs font-bold text-red-800 block mb-1">AFFECTED AREA</span>
                                            <span className="font-bold text-red-700">{result.disease_analysis.affected_area_percentage}%</span>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Why? (Analysis Section) */}
                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-lg flex items-center">
                                        <CheckCircle className="mr-2 h-5 w-5 text-gray-700" />
                                        Diagnostic Reasoning
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg border border-gray-100">
                                        {result.disease_analysis.analysis}
                                    </p>

                                    <div className="mt-4">
                                        <span className="text-sm font-bold text-gray-800 mb-2 block">Detected Symptoms:</span>
                                        <div className="flex flex-wrap gap-2">
                                            {result.disease_analysis.symptoms_detected?.map((symptom: string, idx: number) => (
                                                <span key={idx} className="px-3 py-1 bg-white border border-gray-200 rounded-full text-sm text-gray-700">
                                                    {symptom}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Solution Section */}
                            <Card className="border-blue-200 bg-blue-50/50">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-blue-900 flex items-center">
                                        <FlaskConical className="mr-2 h-5 w-5 text-blue-700" />
                                        Recommended Solutions
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="grid grid-cols-1 gap-3">
                                        <div className="bg-white p-3 rounded-lg border border-blue-100 shadow-sm">
                                            <span className="text-xs font-black text-blue-800 tracking-widest block mb-1">CHEMICAL TREATMENT</span>
                                            <p className="text-gray-800 font-medium">{result.disease_analysis.chemical_treatment}</p>
                                        </div>
                                        <div className="bg-white p-3 rounded-lg border border-blue-100 shadow-sm">
                                            <span className="text-xs font-black text-blue-800 tracking-widest block mb-1">ORGANIC ALTERNATIVE</span>
                                            <p className="text-gray-800 font-medium">{result.disease_analysis.organic_treatment}</p>
                                        </div>
                                        <div className="bg-white p-3 rounded-lg border border-blue-100 shadow-sm">
                                            <span className="text-xs font-black text-blue-800 tracking-widest block mb-1">DOSAGE & APPLICATION</span>
                                            <p className="text-gray-800 font-medium">{result.disease_analysis.dosage}</p>
                                        </div>
                                    </div>

                                    <div className="pt-2 border-t border-blue-100">
                                        <span className="text-sm font-bold text-blue-900 mb-2 block">Preventative Measures:</span>
                                        <ul className="space-y-1">
                                            {result.disease_analysis.recommendations?.map((rec: string, idx: number) => (
                                                <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                                                    <div className="h-1.5 w-1.5 rounded-full bg-blue-400 mt-1.5" />
                                                    {rec}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Weather Card */}
                            <Card className="border-orange-100">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-lg">Environmental Risk Context</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="flex justify-between items-center mb-3">
                                        <span className="text-gray-600 font-medium italic">Current Local Risk:</span>
                                        <span className={`font-bold px-3 py-1 rounded-full text-sm ${result.weather_risk.infection_risk_level === 'High' ? 'bg-red-100 text-red-700' :
                                            result.weather_risk.infection_risk_level === 'Moderate' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                                            }`}>
                                            {result.weather_risk.infection_risk_level?.toUpperCase()}
                                        </span>
                                    </div>
                                    <div className="p-3 bg-orange-50/50 rounded-lg border border-orange-100">
                                        <p className="text-sm text-gray-700 leading-snug">
                                            <strong className="text-orange-900">Advisory:</strong> {result.weather_risk.spraying_advice}
                                        </p>
                                    </div>
                                </CardContent>
                            </Card>
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}
