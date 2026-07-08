'use client'

import { useState, useEffect } from "react"
import {
    Cloud,
    Bell,
    Camera,
    BookOpen,
    ShoppingCart,
    MapPin,
    BarChart3,
    MessageCircle,
    Wind,
    Droplets,
    AlertTriangle,
    ChevronRight,
    Sprout,
    Wheat,
    Leaf,
    Lightbulb,
    Loader2
} from "lucide-react"
import Link from "next/link"
import api from "@/lib/api"

import { Card, CardContent } from "@/components/ui/card"
import { useLanguage } from "@/context/LanguageContext"

export default function FarmerDashboard() {
    const { lang, setLang, t } = useLanguage()
    const [weather, setWeather] = useState<any>(null)
    const [loadingWeather, setLoadingWeather] = useState(true)

    useEffect(() => {
        const fetchWeatherAtLocation = async (lat: number, lon: number) => {
            try {
                const res = await api.post("/advisory/get-advice", {
                    lat,
                    lon,
                    crop_name: "General",
                    growth_stage: "Vegetative"
                })
                setWeather(res.data.weather)
            } catch (err) {
                console.error("Dashboard weather error", err)
            } finally {
                setLoadingWeather(false)
            }
        }

        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => fetchWeatherAtLocation(pos.coords.latitude, pos.coords.longitude),
                () => fetchWeatherAtLocation(18.5204, 73.8567) // Fallback to Pune
            )
        } else {
            fetchWeatherAtLocation(18.5204, 73.8567)
        }
    }, [])

    return (
        <div className="flex-1 bg-gray-50 min-h-screen pb-20 md:pb-0">
            {/* Custom Header for Mobile/Page View */}
            <div className="bg-white px-6 py-4 flex items-center justify-between sticky top-0 z-10 shadow-sm md:hidden">
                <div className="flex items-center gap-2">
                    <div className="bg-green-700 p-1.5 rounded-lg">
                        <Leaf className="h-5 w-5 text-white fill-white" />
                    </div>
                    <span className="font-bold text-lg text-gray-900">AgroCure AI</span>
                </div>
                <div className="flex items-center gap-3">
                    <button 
                        onClick={() => setLang(lang === 'en' ? 'hi' : 'en')}
                        className="bg-green-50 px-3 py-1 rounded-full text-green-700 text-sm font-bold border border-green-100"
                    >
                        {lang === 'en' ? 'EN' : 'HI'}
                    </button>
                    <div className="bg-gray-100 p-2 rounded-full">
                        <Cloud className="h-5 w-5 text-gray-600" />
                    </div>
                    <div className="bg-gray-100 p-2 rounded-full relative">
                        <Bell className="h-5 w-5 text-gray-600" />
                        <span className="absolute top-0 right-0 h-2.5 w-2.5 bg-red-500 rounded-full border-2 border-white"></span>
                    </div>
                </div>
            </div>

            <div className="p-4 md:p-8 space-y-6 max-w-5xl mx-auto">

                {/* Hero Section */}
                <div className="rounded-3xl bg-gradient-to-r from-green-800 to-green-900 p-6 md:p-10 text-white shadow-lg relative overflow-hidden">
                    <div className="relative z-10">
                        <h1 className="text-2xl md:text-3xl font-bold mb-2">{t('protectCrops')}</h1>
                        <p className="text-green-100 text-sm md:text-base opacity-90">{t('scanDetectCure')}</p>
                    </div>
                    {/* Decorative circles */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-green-700 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
                    <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-green-600 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
                </div>

                {/* Weather Widget */}
                <Card className="rounded-2xl border-none shadow-sm overflow-hidden">
                    <CardContent className="p-0">
                        <div className="flex flex-col md:flex-row md:items-center justify-between p-5 gap-4">
                            <div className="flex items-center gap-4">
                                <div className="bg-yellow-100 p-3 rounded-full">
                                    {loadingWeather ? (
                                        <Loader2 className="h-8 w-8 text-yellow-600 animate-spin" />
                                    ) : (
                                        <Cloud className="h-8 w-8 text-yellow-600 fill-yellow-600" />
                                    )}
                                </div>
                                <div>
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-2xl font-bold text-gray-900">
                                            {loadingWeather ? '--' : `${weather?.temp || 0}`}°C
                                        </span>
                                        <span className="text-gray-500 font-medium">— {t('weatherPartlyCloudy')}</span>
                                    </div>
                                    <div className="flex gap-3 text-xs text-gray-400 mt-1">
                                        <span className="flex items-center gap-1">
                                            <Droplets className="h-3 w-3" /> {t('weatherHumidity')}: {weather?.humidity || '--'}%
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Wind className="h-3 w-3" /> {t('weatherWind')}: 12 km/h
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-orange-50 px-4 py-2 rounded-xl border border-orange-100 flex items-center gap-2 self-start md:self-center">
                                <AlertTriangle className="h-4 w-4 text-orange-600 fill-orange-600" />
                                <span className="text-orange-700 font-bold text-sm">{t('fungalRisk')}</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Quick Actions */}
                <div>
                    <h3 className="text-lg font-bold text-gray-800 mb-4">{t('quickActions')}</h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {/* Scalable Card: Scan Disease */}
                        <Link href="/farmer/disease-check" className="col-span-1">
                            <Card className="h-full bg-green-800 border-none shadow-md hover:shadow-lg transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-white/20 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <Camera className="h-5 w-5 text-white" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white text-base">{t('scanDisease')}</h4>
                                        <p className="text-green-200 text-xs mt-1">{t('aiPowered')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Disease Library */}
                        <Link href="/farmer/library">
                            <Card className="h-full border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-blue-100 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <BookOpen className="h-5 w-5 text-blue-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-800 text-base">{t('diseaseLibrary')}</h4>
                                        <p className="text-gray-400 text-xs mt-1">{t('browseAll')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Buy Medicine */}
                        <Link href="/farmer/market" className="col-span-1">
                            <Card className="h-full border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-purple-100 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <ShoppingCart className="h-5 w-5 text-purple-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-800 text-base">{t('buyMedicine')}</h4>
                                        <p className="text-gray-400 text-xs mt-1">{t('orderOnline')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Nearby Stores */}
                        <Link href="/farmer/stores" className="col-span-1">
                            <Card className="h-full border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-red-100 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <MapPin className="h-5 w-5 text-red-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-800 text-base">{t('nearbyStores')}</h4>
                                        <p className="text-gray-400 text-xs mt-1">{t('findAgroShops')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Crop Reports */}
                        <Link href="/farmer/reports">
                            <Card className="h-full border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-indigo-100 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <BarChart3 className="h-5 w-5 text-indigo-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-800 text-base">{t('cropReports')}</h4>
                                        <p className="text-gray-400 text-xs mt-1">{t('healthAnalytics')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Talk to Expert */}
                        <Link href="/farmer/expert">
                            <Card className="h-full border-none shadow-sm hover:shadow-md transition-shadow cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-teal-100 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                        <MessageCircle className="h-5 w-5 text-teal-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-800 text-base">{t('talkToExpert')}</h4>
                                        <p className="text-gray-400 text-xs mt-1">{t('getGuidance')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Smart Advisory */}
                        <Link href="/farmer/advisory" className="col-span-1">
                            <Card className="h-full bg-indigo-50 border-indigo-100 border shadow-sm hover:shadow-md transition-all cursor-pointer rounded-2xl group">
                                <CardContent className="p-5 flex flex-col justify-between h-full">
                                    <div className="bg-indigo-600 w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-indigo-600/20">
                                        <Lightbulb className="h-5 w-5 text-white" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-900 text-base">{t('smartAdvisory')}</h4>
                                        <p className="text-indigo-600 font-medium text-[10px] mt-1 uppercase tracking-wider">{t('aiPowered')}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>
                    </div>
                </div>

                {/* Recent Scans */}
                <div>
                    <h3 className="text-lg font-bold text-gray-800 mb-4">{t('recentScans')}</h3>
                    <div className="space-y-3">
                        {/* Item 1 */}
                        <Card className="rounded-2xl border-none shadow-sm hover:bg-gray-50 transition-colors cursor-pointer">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="bg-red-100 p-3 rounded-xl">
                                        <div className="h-6 w-6 rounded-full bg-red-500/20 flex items-center justify-center">
                                            <div className="h-4 w-4 rounded-full bg-red-500"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-900">Tomato</h4>
                                        <p className="text-gray-500 text-xs">Early Blight</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="bg-red-100 text-red-600 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wide">{t('severityHigh')}</span>
                                    <p className="text-gray-400 text-[10px] mt-1">2 {t('hoursAgo')}</p>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Item 2 */}
                        <Card className="rounded-2xl border-none shadow-sm hover:bg-gray-50 transition-colors cursor-pointer">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="bg-yellow-100 p-3 rounded-xl">
                                        <Wheat className="h-6 w-6 text-yellow-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-900">Rice</h4>
                                        <p className="text-gray-500 text-xs">Blast Disease</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="bg-red-100 text-red-600 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wide">{t('severityHigh')}</span>
                                    <p className="text-gray-400 text-[10px] mt-1">{t('yesterdayLocal')}</p>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Item 3 */}
                        <Card className="rounded-2xl border-none shadow-sm hover:bg-gray-50 transition-colors cursor-pointer">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="bg-green-100 p-3 rounded-xl">
                                        <Sprout className="h-6 w-6 text-green-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-gray-900">Wheat</h4>
                                        <p className="text-gray-500 text-xs">Healthy</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="bg-green-100 text-green-600 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wide">{t('severityNone')}</span>
                                    <p className="text-gray-400 text-[10px] mt-1">3 {t('daysAgo')}</p>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>

            </div>
        </div>
    )
}
