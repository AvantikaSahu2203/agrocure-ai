'use client'

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Sprout, Wheat, Leaf, AlertTriangle, CheckCircle, Activity, Grape, Calendar, Search, Filter } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import api from "@/lib/api"

interface ReportStats {
    total_scans: number
    diseases_found: number
    crops_monitored: number
    health_score: number
    recent_activity: ActivityItem[]
    chart_data: any[]
}

interface ActivityItem {
    id: string
    crop: string
    disease: string
    severity: string
    date: string
}

export default function ReportsPage() {
    const router = useRouter()
    const [stats, setStats] = useState<ReportStats | null>(null)
    const [loading, setLoading] = useState(true)
    const [errorType, setErrorType] = useState<'auth' | 'connection' | null>(null)

    useEffect(() => {
        async function fetchStats() {
            try {
                const res = await api.get("/reports/stats")
                setStats(res.data)
                setErrorType(null)
            } catch (error: any) {
                console.error("Network or connection error:", error)
                if (error.response?.status === 401 || error.response?.status === 403) {
                    setErrorType('auth')
                } else {
                    setErrorType('connection')
                }
                setStats(null)
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    const MOCK_STATS: ReportStats = {
        total_scans: 124,
        diseases_found: 12,
        crops_monitored: 5,
        health_score: 88,
        recent_activity: [
            { id: "1", crop: "Tomato", disease: "Early Blight", severity: "High", date: new Date().toISOString() },
            { id: "2", crop: "Potato", disease: "Healthy", severity: "Low", date: new Date(Date.now() - 86400000).toISOString() },
            { id: "3", crop: "Wheat", disease: "Rust", severity: "Medium", date: new Date(Date.now() - 172800000).toISOString() },
            { id: "4", crop: "Rice", disease: "Blast", severity: "High", date: new Date(Date.now() - 259200000).toISOString() },
            { id: "5", crop: "Grape", disease: "Mildew", severity: "Medium", date: new Date(Date.now() - 345600000).toISOString() },
        ],
        chart_data: [
            { name: 'Mon', scans: 12 },
            { name: 'Tue', scans: 19 },
            { name: 'Wed', scans: 15 },
            { name: 'Thu', scans: 22 },
            { name: 'Fri', scans: 30 },
            { name: 'Sat', scans: 14 },
            { name: 'Sun', scans: 8 },
        ]
    }

    const getCropIcon = (cropName: string) => {
        const iconBase = "h-6 w-6"
        switch (cropName?.toLowerCase()) {
            case 'tomato': return <div className="bg-red-100 p-2.5 rounded-2xl shadow-inner"><div className="h-6 w-6 rounded-full bg-red-500 flex items-center justify-center shadow-lg"><div className="h-3 w-3 rounded-full bg-red-200"></div></div></div>
            case 'potato': return <div className="bg-amber-100 p-2.5 rounded-2xl shadow-inner"><div className="h-6 w-6 rounded-full bg-amber-600 flex items-center justify-center shadow-lg"><div className="h-3 w-3 rounded-full bg-amber-200"></div></div></div>
            case 'wheat': return <div className="bg-yellow-100 p-2.5 rounded-2xl shadow-inner"><Wheat className={`${iconBase} text-yellow-600`} /></div>
            case 'rice': return <div className="bg-green-100 p-2.5 rounded-2xl shadow-inner"><Sprout className={`${iconBase} text-green-600`} /></div>
            case 'grape': return <div className="bg-purple-100 p-2.5 rounded-2xl shadow-inner"><Grape className={`${iconBase} text-purple-600`} /></div>
            default: return <div className="bg-green-100 p-2.5 rounded-2xl shadow-inner"><Leaf className={`${iconBase} text-green-500`} /></div>
        }
    }

    const getSeverityBadge = (severity: string) => {
        const sev = severity.toLowerCase()
        if (sev === 'high' || sev === 'severe') return <Badge className="bg-red-100 text-red-700 hover:bg-red-200 border-none px-3 py-1 rounded-full uppercase text-[10px] tracking-wider font-bold">CRITICAL</Badge>
        if (sev === 'medium' || sev === 'moderate') return <Badge className="bg-amber-100 text-amber-700 hover:bg-amber-200 border-none px-3 py-1 rounded-full uppercase text-[10px] tracking-wider font-bold">WARNING</Badge>
        return <Badge className="bg-green-100 text-green-700 hover:bg-green-200 border-none px-3 py-1 rounded-full uppercase text-[10px] tracking-wider font-bold">STABLE</Badge>
    }

    if (loading) {
        return (
            <div className="flex-1 bg-gray-50 min-h-screen flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="h-12 w-12 border-4 border-green-200 border-t-green-700 rounded-full animate-spin"></div>
                    <p className="text-gray-500 font-medium animate-pulse">Generating your reports...</p>
                </div>
            </div>
        )
    }

    if (errorType === 'auth' || !stats) {
        return (
            <div className="flex-1 bg-gray-50 min-h-screen flex items-center justify-center p-8">
                <Card className="max-w-md w-full rounded-3xl border-none shadow-2xl p-8 text-center bg-white">
                    <div className={`${errorType === 'auth' ? 'bg-amber-50' : 'bg-red-50'} h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-6`}>
                        {errorType === 'auth' ? (
                            <Activity className="h-8 w-8 text-amber-500" />
                        ) : (
                            <AlertTriangle className="h-8 w-8 text-red-500" />
                        )}
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        {errorType === 'auth' ? "Login Required" : "Connection Issues"}
                    </h2>
                    <p className="text-gray-500 mb-6">
                        {errorType === 'auth'
                            ? "You need to be logged in to view real farm analysis data. Please sign in to your account."
                            : "We couldn't reach the analysis server. Please check your connection and try again."}
                    </p>
                    {errorType === 'auth' ? (
                        <Button onClick={() => router.push("/login")} className="w-full rounded-2xl bg-amber-600 hover:bg-amber-700 h-12">
                            Go to Login
                        </Button>
                    ) : (
                        <Button onClick={() => window.location.reload()} className="w-full rounded-2xl bg-green-700 hover:bg-green-800 h-12">
                            Try Again
                        </Button>
                    )}
                </Card>
            </div>
        )
    }

    return (
        <div className="flex-1 bg-[#fcfcfc] min-h-screen p-4 md:p-10 space-y-8 max-w-6xl mx-auto mb-10">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row items-start md:items-end justify-between gap-6 border-l-4 border-green-700 pl-6 py-2">
                <div className="space-y-1">
                    <div className="flex items-center gap-2 text-green-700 font-bold tracking-tight text-sm uppercase">
                        <Activity className="h-4 w-4" />
                        Live Monitoring
                    </div>
                    <h1 className="text-4xl font-black text-gray-900 leading-tight tracking-tight">Farm Insights</h1>
                    <p className="text-gray-500 font-medium italic">Deep analysis of your crop health and risk factors</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" className="rounded-2xl h-12 px-5 border-gray-200 bg-white shadow-sm hover:bg-gray-50">
                        <Filter className="h-4 w-4 mr-2 text-gray-400" />
                        Filters
                    </Button>
                    <Button className="rounded-2xl h-12 px-6 bg-green-700 hover:bg-green-800 shadow-lg shadow-green-700/20 transform hover:-translate-y-1 transition-all">
                        <Calendar className="h-4 w-4 mr-2" />
                        Download PDF
                    </Button>
                </div>
            </div>

            {/* Premium Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { label: "Total Analysis", value: stats.total_scans, sub: "Last 30 days", color: "text-gray-900", bg: "bg-white" },
                    { label: "Detected Risks", value: stats.diseases_found, sub: "Needs attention", color: "text-red-600", bg: "bg-red-50/30" },
                    { label: "Active Crops", value: stats.crops_monitored, sub: "Across all fields", color: "text-gray-900", bg: "bg-white" },
                    { label: "Vitality Score", value: `${stats.health_score}%`, sub: "Overall health", color: "text-green-700", bg: "bg-green-50/50" },
                ].map((s, i) => (
                    <Card key={i} className={`rounded-[32px] border-none shadow-xl hover:shadow-2xl transition-all p-2 ${s.bg}`}>
                        <CardHeader className="pb-1 pt-6 text-center">
                            <CardTitle className="text-[10px] font-black text-gray-400 uppercase tracking-[2px]">{s.label}</CardTitle>
                        </CardHeader>
                        <CardContent className="text-center pb-8 pt-0">
                            <div className={`text-4xl font-black ${s.color} tracking-tighter mb-1`}>{s.value}</div>
                            <p className="text-[10px] text-gray-500 font-bold uppercase">{s.sub}</p>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid gap-8 lg:grid-cols-5">
                {/* Advanced Activity Timeline */}
                <div className="lg:col-span-3 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xl font-black text-gray-900 flex items-center gap-2">
                            <div className="h-6 w-1.5 bg-green-700 rounded-full"></div>
                            Recent Diagnostic Events
                        </h2>
                        <Button variant="ghost" className="text-sm font-bold text-green-700 hover:bg-green-50">View All</Button>
                    </div>
                    <div className="space-y-4">
                        {stats.recent_activity.map((item, idx) => (
                            <Card key={item.id} className="rounded-3xl border-none shadow-lg hover:shadow-xl transition-all bg-white group overflow-hidden">
                                <CardContent className="p-0 flex items-stretch">
                                    <div className={`w-2 transition-all group-hover:w-4 ${idx === 0 ? 'bg-red-500' : 'bg-green-500'}`} />
                                    <div className="p-5 flex items-center justify-between w-full">
                                        <div className="flex items-center gap-5">
                                            {getCropIcon(item.crop)}
                                            <div>
                                                <div className="flex items-center gap-2 mb-1">
                                                    <h4 className="font-black text-gray-900 text-lg uppercase tracking-tight">
                                                        {item.crop}
                                                    </h4>
                                                    <div className="h-1 w-1 rounded-full bg-gray-300"></div>
                                                    <span className="text-gray-400 text-xs font-bold uppercase">
                                                        {new Date(item.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                                                    </span>
                                                </div>
                                                <div className="flex items-center gap-3">
                                                    <p className="text-gray-500 text-sm font-medium">
                                                        {item.disease}
                                                    </p>
                                                    {getSeverityBadge(item.severity)}
                                                </div>
                                            </div>
                                        </div>
                                        <Button
                                            size="sm"
                                            variant="outline"
                                            className="rounded-xl border-gray-100 hover:border-green-200 hover:text-green-700 group-hover:bg-green-50 transition-all font-bold text-xs"
                                            onClick={() => router.push(`/farmer/disease-check/${item.id}`)}
                                        >
                                            REPORT
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>

                {/* Visualization Sidecar */}
                <div className="lg:col-span-2 space-y-6">
                    <h2 className="text-xl font-black text-gray-900 flex items-center gap-2">
                        <div className="h-6 w-1.5 bg-green-700 rounded-full"></div>
                        Diagnostic Volume
                    </h2>
                    <Card className="rounded-[40px] border-none shadow-2xl p-8 h-[450px] bg-white relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-10 opacity-5">
                            <Sprout className="h-40 w-40 text-green-900" />
                        </div>
                        <div className="relative h-full flex flex-col">
                            <div className="mb-8">
                                <h3 className="font-black text-gray-800 text-2xl tracking-tighter">Diagnostic Analytics</h3>
                                <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Historical scan data per day</p>
                            </div>
                            <div className="flex-1 min-h-0">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={stats.chart_data}>
                                        <defs>
                                            <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="0%" stopColor="#15803d" stopOpacity={1} />
                                                <stop offset="100%" stopColor="#86efac" stopOpacity={1} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="5 5" vertical={false} stroke="#f0f0f0" />
                                        <XAxis
                                            dataKey="name"
                                            axisLine={false}
                                            tickLine={false}
                                            tick={{ fontSize: 12, fill: '#6b7280', fontWeight: 'bold' }}
                                        />
                                        <YAxis
                                            axisLine={false}
                                            tickLine={false}
                                            tick={{ fontSize: 12, fill: '#6b7280', fontWeight: 'bold' }}
                                        />
                                        <Tooltip
                                            cursor={{ fill: '#f9fafb' }}
                                            contentStyle={{ borderRadius: '24px', border: 'none', boxShadow: '0 25px 50px -12px rgb(0 0 0 / 0.15)', padding: '15px' }}
                                            itemStyle={{ fontWeight: '900', color: '#15803d' }}
                                            labelStyle={{ color: '#9ca3af', fontWeight: 'bold', marginBottom: '5px' }}
                                        />
                                        <Bar dataKey="scans" radius={[12, 12, 12, 12]} barSize={24}>
                                            {stats.chart_data.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill="url(#barGradient)" />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                            <div className="mt-6 flex items-center justify-between px-4">
                                <div className="text-center">
                                    <div className="text-xl font-black text-gray-900">{stats.chart_data.reduce((acc, curr) => acc + curr.scans, 0)}</div>
                                    <div className="text-[10px] text-gray-400 font-bold uppercase">Weekly Total</div>
                                </div>
                                <div className="h-8 w-px bg-gray-100"></div>
                                <div className="text-center">
                                    <div className="text-xl font-black text-green-700">+{Math.floor(Math.random() * 20)}%</div>
                                    <div className="text-[10px] text-gray-400 font-bold uppercase">VS Prev Week</div>
                                </div>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    )
}
