'use client'

import { useState } from 'react'
import { Upload, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"

export default function DiseaseDetection() {
    const [selectedImage, setSelectedImage] = useState<File | null>(null)
    const [previewUrl, setPreviewUrl] = useState<string>('')
    const [cropName, setCropName] = useState('')
    const [region, setRegion] = useState('')
    const [weather, setWeather] = useState('')
    const [growthStage, setGrowthStage] = useState('')
    const [analyzing, setAnalyzing] = useState(false)
    const [result, setResult] = useState<any>(null)
    const [error, setError] = useState('')

    const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            setSelectedImage(file)
            setPreviewUrl(URL.createObjectURL(file))
            setResult(null)
            setError('')
        }
    }

    const handleAnalyze = async () => {
        if (!selectedImage || !cropName) {
            setError('Please select an image and enter crop name')
            return
        }

        setAnalyzing(true)
        setError('')

        try {
            const formData = new FormData()
            formData.append('image', selectedImage)
            formData.append('crop_name', cropName)
            if (region) formData.append('region', region)
            if (weather) formData.append('weather', weather)
            if (growthStage) formData.append('growth_stage', growthStage)

            const response = await fetch('http://localhost:8000/api/v1/disease-ai/analyze', {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}))
                throw new Error(errorData.detail || 'Analysis failed with status ' + response.status)
            }

            const data = await response.json()
            setResult(data)
        } catch (err: any) {
            const errorMessage = err.message || 'Unknown error occurred'
            setError(`Failed to analyze image: ${errorMessage}`)
            console.error("Disease Detection Error:", err)
        } finally {
            setAnalyzing(false)
        }
    }

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'mild': return 'text-yellow-600 bg-yellow-50'
            case 'moderate': return 'text-orange-600 bg-orange-50'
            case 'severe': return 'text-red-600 bg-red-50'
            default: return 'text-gray-600 bg-gray-50'
        }
    }

    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Disease Detection</h2>

                {/* Image Upload */}
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Upload Crop Image
                    </label>
                    <div className="flex items-center justify-center w-full">
                        <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                            {previewUrl ? (
                                <img src={previewUrl} alt="Preview" className="h-full object-contain" />
                            ) : (
                                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                    <Upload className="w-12 h-12 text-gray-400 mb-3" />
                                    <p className="mb-2 text-sm text-gray-500">
                                        <span className="font-semibold">Click to upload</span> or drag and drop
                                    </p>
                                    <p className="text-xs text-gray-500">PNG, JPG or JPEG</p>
                                </div>
                            )}
                            <input
                                type="file"
                                className="hidden"
                                accept="image/*"
                                onChange={handleImageSelect}
                            />
                        </label>
                    </div>
                </div>

                {/* Input Fields */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Crop Name *
                        </label>
                        <input
                            type="text"
                            value={cropName}
                            onChange={(e) => setCropName(e.target.value)}
                            placeholder="e.g., Tomato, Wheat, Rice"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Region
                        </label>
                        <input
                            type="text"
                            value={region}
                            onChange={(e) => setRegion(e.target.value)}
                            placeholder="e.g., Maharashtra, Punjab"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Weather Conditions
                        </label>
                        <input
                            type="text"
                            value={weather}
                            onChange={(e) => setWeather(e.target.value)}
                            placeholder="e.g., Humid, Dry, Rainy"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Growth Stage
                        </label>
                        <input
                            type="text"
                            value={growthStage}
                            onChange={(e) => setGrowthStage(e.target.value)}
                            placeholder="e.g., Vegetative, Flowering"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                        />
                    </div>
                </div>

                {error && (
                    <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-center gap-2 text-red-700">
                        <AlertCircle className="w-5 h-5" />
                        {error}
                    </div>
                )}

                <Button
                    onClick={handleAnalyze}
                    disabled={analyzing || !selectedImage || !cropName}
                    className="w-full"
                >
                    {analyzing ? (
                        <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        'Analyze Disease'
                    )}
                </Button>
            </div>

            {/* Results */}
            {result && (
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center gap-2 mb-4">
                        <CheckCircle className="w-6 h-6 text-green-600" />
                        <h3 className="text-xl font-bold text-gray-900">Analysis Results</h3>
                    </div>

                    <div className="space-y-4">
                        {/* Disease Info */}
                        <div className="border-b pb-4">
                            <h4 className="text-lg font-semibold text-gray-900 mb-2">{result.disease_name}</h4>
                            <p className="text-sm text-gray-600 italic mb-2">{result.scientific_name}</p>
                            <div className="flex items-center gap-4">
                                <div>
                                    <span className="text-sm text-gray-600">Confidence: </span>
                                    <span className="font-semibold text-green-600">{(result.confidence * 100).toFixed(0)}%</span>
                                </div>
                                <div>
                                    <span className="text-sm text-gray-600">Severity: </span>
                                    <span className={`px-2 py-1 rounded text-sm font-semibold ${getSeverityColor(result.severity)}`}>
                                        {result.severity.toUpperCase()}
                                    </span>
                                </div>
                                <div>
                                    <span className="text-sm text-gray-600">Affected Area: </span>
                                    <span className="font-semibold">{result.affected_area_percentage}%</span>
                                </div>
                            </div>
                        </div>

                        {/* Analysis */}
                        <div>
                            <h5 className="font-semibold text-gray-900 mb-2">Analysis</h5>
                            <p className="text-gray-700">{result.analysis}</p>
                        </div>

                        {/* Symptoms */}
                        <div>
                            <h5 className="font-semibold text-gray-900 mb-2">Detected Symptoms</h5>
                            <ul className="list-disc list-inside space-y-1">
                                {result.symptoms_detected.map((symptom: string, idx: number) => (
                                    <li key={idx} className="text-gray-700">{symptom}</li>
                                ))}
                            </ul>
                        </div>

                        {/* Recommendations */}
                        <div>
                            <h5 className="font-semibold text-gray-900 mb-2">Treatment Recommendations</h5>
                            <ol className="list-decimal list-inside space-y-1">
                                {result.recommendations.map((rec: string, idx: number) => (
                                    <li key={idx} className="text-gray-700">{rec}</li>
                                ))}
                            </ol>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
