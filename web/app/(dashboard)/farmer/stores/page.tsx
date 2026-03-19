'use client'

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MapPin, Phone, Star, Navigation, Search, Loader2, AlertCircle } from "lucide-react"

export default function NearbyStoresPage() {
    const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [searchQuery, setSearchQuery] = useState("")

    // Partner stores mock data (kept for UI richness)
    const partnerStores = [
        {
            id: 1,
            name: "AgroStar Kendra",
            address: "123 Main St, Pune, Maharashtra",
            phone: "+91 98765 43210",
            rating: 4.5,
            distance: "1.2 km",
        },
        {
            id: 2,
            name: "Kisan Seva Kendra",
            address: "456 Market Rd, Pune, Maharashtra",
            phone: "+91 98765 12345",
            rating: 4.2,
            distance: "2.5 km",
        },
    ]

    const handleGetLocation = () => {
        setLoading(true)
        setError(null)

        if (!navigator.geolocation) {
            setError("Geolocation is not supported by your browser.")
            setLoading(false)
            return
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                setLocation({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                })
                setLoading(false)
            },
            (err) => {
                console.error("Geolocation Error:", err.message, err.code)
                let errorMessage = "Unable to retrieve your location."
                if (err.code === 1) errorMessage = "Location permission denied. Please allow access."
                if (err.code === 2) errorMessage = "Location unavailable. Please check your connection."
                if (err.code === 3) errorMessage = "Location request timed out."

                setError(errorMessage)
                setLoading(false)
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        )
    }

    const openGoogleMaps = (query: string) => {
        let url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`
        if (location) {
            url += `+near+${location.lat},${location.lng}`
        }
        window.open(url, '_blank')
    }

    return (
        <div className="flex-1 space-y-6 p-4 md:p-8 pt-6 max-w-6xl mx-auto">
            <div className="flex flex-col gap-2">
                <h2 className="text-3xl font-bold tracking-tight text-gray-900">Find Nearby Stores</h2>
                <p className="text-gray-500">Locate agricultural shops, pesticide dealers, and fertilizer monitors near you.</p>
            </div>

            {/* Main Action Card */}
            <Card className="border-green-100 shadow-md overflow-hidden">
                <div className="bg-green-600 h-2"></div>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <MapPin className="h-5 w-5 text-green-600" />
                        {location ? "Location Detected" : "Locate Yourself"}
                    </CardTitle>
                    <CardDescription>
                        {location
                            ? `Lat: ${location.lat.toFixed(4)}, Lng: ${location.lng.toFixed(4)}`
                            : "Allow location access to find the closest stores automatically."}
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    {!location ? (
                        <div className="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                            {error ? (
                                <div className="text-red-500 flex flex-col items-center gap-2">
                                    <AlertCircle className="h-8 w-8" />
                                    <p>{error}</p>
                                    <Button variant="outline" onClick={handleGetLocation} className="mt-2">Try Again</Button>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center gap-4">
                                    <div className="p-4 bg-green-100 rounded-full">
                                        <MapPin className="h-8 w-8 text-green-600" />
                                    </div>
                                    <p className="text-gray-600 max-w-sm">
                                        We need your location to show you the nearest agricultural supply stores.
                                    </p>
                                    <Button
                                        onClick={handleGetLocation}
                                        className="bg-green-600 hover:bg-green-700 w-full max-w-xs"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                                Detecting Location...
                                            </>
                                        ) : (
                                            "Detect My Location"
                                        )}
                                    </Button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="grid gap-4 md:grid-cols-2">
                            <Button
                                className="h-16 text-lg bg-blue-600 hover:bg-blue-700"
                                onClick={() => openGoogleMaps("agriculture medicine store")}
                            >
                                <Search className="mr-2 h-6 w-6" />
                                Find Agri Medicine Stores
                            </Button>
                            <Button
                                className="h-16 text-lg bg-emerald-600 hover:bg-emerald-700"
                                onClick={() => openGoogleMaps("fertilizer shop")}
                            >
                                <Search className="mr-2 h-6 w-6" />
                                Find Fertilizer Shops
                            </Button>

                            <div className="col-span-full mt-4">
                                <p className="text-sm font-medium mb-2">Search for specific product:</p>
                                <div className="flex gap-2">
                                    <Input
                                        placeholder="e.g. Urea, Mancozeb, Seeds..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                    />
                                    <Button onClick={() => openGoogleMaps(searchQuery || "agriculture store")}>
                                        Search
                                    </Button>
                                </div>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Partner Stores / Result Placeholder */}
            <div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Featured Partner Stores</h3>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {partnerStores.map((store) => (
                        <Card key={store.id} className="hover:shadow-md transition-shadow">
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle className="text-lg font-bold">{store.name}</CardTitle>
                                        <CardDescription className="flex items-center mt-1">
                                            <MapPin className="h-3 w-3 mr-1" />
                                            {store.distance}
                                        </CardDescription>
                                    </div>
                                    <div className="flex items-center bg-yellow-100 px-2 py-1 rounded text-xs font-bold text-yellow-700">
                                        <Star className="h-3 w-3 mr-1 fill-yellow-700" />
                                        {store.rating}
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="text-sm text-gray-600 space-y-2">
                                    <p>{store.address}</p>
                                    <div className="flex items-center">
                                        <Phone className="h-4 w-4 mr-2" />
                                        {store.phone}
                                    </div>
                                </div>
                                <Button className="w-full mt-4" variant="outline" onClick={() => openGoogleMaps(store.name)}>
                                    <Navigation className="h-4 w-4 mr-2" />
                                    Navigate
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    )
}
