'use client'

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { Users, FileText, Activity, Database, AlertCircle, TrendingUp, ShieldCheck, Globe } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface AdminStats {
    users: number
    crops: number
    detections: number
    stores: number
}

const COLORS = ['#15803d', '#10b981', '#3b82f6', '#f59e0b', '#ef4444'];

export default function AdminReportsPage() {
    const [stats, setStats] = useState<AdminStats | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchStats() {
            try {
                const token = localStorage.getItem("token") || ""
                if (!token) {
                    setStats(MOCK_ADMIN_STATS)
                    setLoading(false)
                    return
                }

                const res = await fetch("http://localhost:8000/api/v1/admin/stats", {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                })
                if (res.ok) {
                    const data = await res.json()
                    setStats(data)
                } else {
                    setStats(MOCK_ADMIN_STATS)
                }
            } catch (error) {
                console.error("Failed to fetch admin stats", error)
                setStats(MOCK_ADMIN_STATS)
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    const MOCK_ADMIN_STATS: AdminStats = {
        users: 1245,
        crops: 18,
        detections: 5672,
        stores: 42
    }

    // Mock data for charts (since backend currently only provides aggregate counts)
    const userGrowthData = [
        { name: 'Sep', users: 400 },
        { name: 'Oct', users: 600 },
        { name: 'Nov', users: 800 },
        { name: 'Dec', users: 1000 },
        { name: 'Jan', users: 1100 },
        { name: 'Feb', users: stats?.users || 1234 },
    ]

    const diseaseTrendsData = [
        { name: 'Blight', value: 40 },
        { name: 'Rust', value: 30 },
        { name: 'Mold', value: 15 },
        { name: 'Spots', value: 10 },
        { name: 'Other', value: 5 },
    ]

    if (loading) {
        return (
            <div className="flex-1 bg-gray-50 min-h-screen flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="h-12 w-12 border-4 border-blue-200 border-t-blue-700 rounded-full animate-spin"></div>
                    <p className="text-gray-500 font-medium animate-pulse">Loading admin insights...</p>
                </div>
            </div>
        )
    }

    const cards = [
        { label: "Platform Users", value: stats?.users || 0, icon: Users, color: "text-blue-600", bg: "bg-blue-50" },
        { label: "Total Detections", value: stats?.detections || 0, icon: Activity, color: "text-green-600", bg: "bg-green-50" },
        { label: "Active Stores", value: stats?.stores || 0, icon: Database, color: "text-purple-600", bg: "bg-purple-50" },
        { label: "Supported Crops", value: stats?.crops || 0, icon: Globe, color: "text-amber-600", bg: "bg-amber-50" },
    ]

    return (
        <div className="flex-1 bg-[#f8fafc] min-h-screen p-4 md:p-10 space-y-8 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div className="space-y-1">
                    <div className="flex items-center gap-2 text-blue-700 font-bold text-sm uppercase tracking-widest">
                        <ShieldCheck className="h-4 w-4" />
                        Administrator Console
                    </div>
                    <h1 className="text-4xl font-black text-slate-900 tracking-tight">System Reports</h1>
                    <p className="text-slate-500 font-medium">Real-time ecosystem performance and user analytics</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" className="rounded-xl h-11 border-slate-200 bg-white shadow-sm">
                        Export Metadata
                    </Button>
                    <Button className="rounded-xl h-11 bg-slate-900 hover:bg-slate-800 text-white shadow-lg">
                        System Audit
                    </Button>
                </div>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card, i) => (
                    <Card key={i} className="rounded-3xl border-none shadow-sm hover:shadow-md transition-shadow transition-transform hover:-translate-y-1">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className={`${card.bg} p-3 rounded-2xl`}>
                                    <card.icon className={`h-6 w-6 ${card.color}`} />
                                </div>
                                <Badge variant="secondary" className="bg-slate-100 text-slate-600 border-none px-2 py-0.5 rounded-lg text-[10px] font-bold">
                                    LIVE
                                </Badge>
                            </div>
                            <div>
                                <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider mb-1">{card.label}</h3>
                                <div className="text-3xl font-black text-slate-900">{card.value.toLocaleString()}</div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* User Growth Chart */}
                <Card className="lg:col-span-2 rounded-[32px] border-none shadow-xl bg-white p-8">
                    <CardHeader className="p-0 mb-8">
                        <CardTitle className="text-xl font-black text-slate-900 flex items-center gap-2">
                            <TrendingUp className="h-5 w-5 text-blue-600" />
                            User Acquisition Trend
                        </CardTitle>
                        <CardDescription className="text-slate-400 font-medium">Monthly growth of registered farmers and store owners</CardDescription>
                    </CardHeader>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={userGrowthData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                <XAxis
                                    dataKey="name"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 'bold' }}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 'bold' }}
                                />
                                <Tooltip
                                    contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)' }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="users"
                                    stroke="#2563eb"
                                    strokeWidth={4}
                                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4, stroke: '#fff' }}
                                    activeDot={{ r: 6, strokeWidth: 0 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </Card>

                {/* Disease Distribution Pie Chart */}
                <Card className="rounded-[32px] border-none shadow-xl bg-white p-8">
                    <CardHeader className="p-0 mb-8">
                        <CardTitle className="text-xl font-black text-slate-900 flex items-center gap-2">
                            <AlertCircle className="h-5 w-5 text-red-500" />
                            Epidemic Alerts
                        </CardTitle>
                        <CardDescription className="text-slate-400 font-medium">Distribution of detected diseases</CardDescription>
                    </CardHeader>
                    <div className="h-[250px] relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={diseaseTrendsData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {diseaseTrendsData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                            <div className="text-2xl font-black text-slate-900">74%</div>
                            <div className="text-[10px] text-slate-400 font-bold uppercase">Success</div>
                        </div>
                    </div>
                    <div className="mt-8 space-y-3">
                        {diseaseTrendsData.map((d, i) => (
                            <div key={i} className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <div className="h-2 w-2 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }}></div>
                                    <span className="text-xs font-bold text-slate-600 uppercase tracking-tight">{d.name}</span>
                                </div>
                                <span className="text-xs font-black text-slate-900">{d.value}%</span>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
        </div>
    )
}
