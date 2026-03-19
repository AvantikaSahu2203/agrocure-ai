'use client'

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
    MessageCircle,
    Video,
    Calendar,
    User,
    Star,
    Clock,
    Award,
    ShieldCheck,
    Search,
    ChevronRight,
    CheckCircle2
} from "lucide-react"
import { Input } from "@/components/ui/input"

const EXPERTS = [
    {
        id: 1,
        name: "Dr. Ramesh Kumar",
        specialty: "Plant Pathologist",
        experience: "15+ Years",
        rating: 4.9,
        reviews: 124,
        status: "Online",
        languages: ["Hindi", "Punjabi", "English"],
        fee: "₹299",
        image: "https://api.dicebear.com/7.x/avataaars/svg?seed=Ramesh"
    },
    {
        id: 2,
        name: "Dr. Anita Sharma",
        specialty: "Soil Scientist",
        experience: "12+ Years",
        rating: 4.8,
        reviews: 98,
        status: "Online",
        languages: ["Hindi", "Marathi", "English"],
        fee: "₹249",
        image: "https://api.dicebear.com/7.x/avataaars/svg?seed=Anita"
    },
    {
        id: 3,
        name: "Prof. S. Venkatesh",
        specialty: "Entomologist",
        experience: "20+ Years",
        rating: 5.0,
        reviews: 215,
        status: "Away",
        languages: ["Tamil", "Telugu", "English"],
        fee: "₹399",
        image: "https://api.dicebear.com/7.x/avataaars/svg?seed=Venkatesh"
    }
]

export default function TalkToExpertPage() {
    const [searchTerm, setSearchTerm] = useState("")

    return (
        <div className="flex-1 bg-[#f0f9f9] min-h-screen p-4 md:p-8 space-y-8 max-w-6xl mx-auto pb-20">
            {/* Header Section */}
            <div className="bg-white rounded-[32px] p-6 md:p-10 shadow-sm border border-teal-50 relative overflow-hidden">
                <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div className="space-y-3">
                        <Badge className="bg-teal-100 text-teal-700 hover:bg-teal-100 border-none px-4 py-1 rounded-full uppercase text-xs font-bold tracking-wider">
                            Verified Specialists
                        </Badge>
                        <h1 className="text-3xl md:text-4xl font-black text-gray-900 leading-tight tracking-tight">
                            Consult with <span className="text-teal-600">Agro Experts</span>
                        </h1>
                        <p className="text-gray-500 font-medium max-w-lg">
                            Get instant guidance on crop diseases, soil health, and pest management from our certified agricultural doctors.
                        </p>
                    </div>
                    <div className="bg-teal-600 p-4 rounded-3xl shadow-xl shadow-teal-600/20 text-white flex items-center gap-4">
                        <div className="h-12 w-12 rounded-full bg-white/20 flex items-center justify-center">
                            <ShieldCheck className="h-6 w-6" />
                        </div>
                        <div>
                            <div className="text-xs font-bold opacity-80 uppercase">Total Experts</div>
                            <div className="text-2xl font-black">45+ Online</div>
                        </div>
                    </div>
                </div>
                {/* Abstract background element */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-teal-50 rounded-full -mr-32 -mt-32 opacity-50" />
            </div>

            {/* Search and Filters */}
            <div className="flex flex-col md:flex-row gap-4">
                <div className="relative flex-1 group">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 group-focus-within:text-teal-600 transition-colors" />
                    <Input
                        placeholder="Search by name or specialty (e.g. Potato, Soil)..."
                        className="h-14 pl-12 rounded-2xl border-none shadow-sm bg-white focus-visible:ring-2 focus-visible:ring-teal-500 transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Button className="h-14 rounded-2xl bg-white text-gray-700 hover:bg-gray-50 shadow-sm px-8 font-bold border-none">
                    Filter by Crop
                </Button>
            </div>

            {/* Experts Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {EXPERTS.filter(e => e.name.toLowerCase().includes(searchTerm.toLowerCase()) || e.specialty.toLowerCase().includes(searchTerm.toLowerCase())).map((expert) => (
                    <Card key={expert.id} className="rounded-[32px] border-none shadow-xl bg-white overflow-hidden group hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                        <CardHeader className="pb-0 pt-8 flex flex-col items-center text-center px-6">
                            <div className="relative">
                                <div className="h-24 w-24 rounded-3xl overflow-hidden bg-teal-50 mb-4 border-4 border-white shadow-lg">
                                    <img src={expert.image} alt={expert.name} className="w-full h-full object-cover" />
                                </div>
                                {expert.status === "Online" && (
                                    <div className="absolute -bottom-1 -right-1 h-5 w-5 bg-green-500 rounded-full border-4 border-white animate-pulse" />
                                )}
                            </div>
                            <CardTitle className="text-xl font-black text-gray-900">{expert.name}</CardTitle>
                            <CardDescription className="text-teal-600 font-bold uppercase text-[10px] tracking-[1px] mt-1">{expert.specialty}</CardDescription>
                        </CardHeader>
                        <CardContent className="pt-6 px-6 pb-8 space-y-6">
                            <div className="grid grid-cols-3 gap-2 bg-gray-50 rounded-2xl p-3">
                                <div className="text-center">
                                    <div className="text-xs font-black text-gray-900">{expert.experience}</div>
                                    <div className="text-[8px] font-bold text-gray-400 uppercase">Exp.</div>
                                </div>
                                <div className="text-center border-x border-gray-200">
                                    <div className="text-xs font-black text-gray-900 flex items-center justify-center gap-1">
                                        {expert.rating} <Star className="h-2.5 w-2.5 fill-yellow-400 text-yellow-400" />
                                    </div>
                                    <div className="text-[8px] font-bold text-gray-400 uppercase">Rating</div>
                                </div>
                                <div className="text-center">
                                    <div className="text-xs font-black text-teal-600">{expert.fee}</div>
                                    <div className="text-[8px] font-bold text-gray-400 uppercase">Consult</div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-gray-500">
                                    <MessageCircle className="h-4 w-4 text-teal-500" />
                                    <span className="text-xs font-medium">{expert.languages.join(", ")}</span>
                                </div>
                                <div className="flex items-center gap-2 text-gray-500">
                                    <Award className="h-4 w-4 text-teal-500" />
                                    <span className="text-xs font-medium">Certified Agro Doctor</span>
                                </div>
                            </div>

                            <div className="flex gap-2">
                                <Button className="flex-1 h-12 rounded-xl bg-teal-600 hover:bg-teal-700 shadow-lg shadow-teal-600/20 text-xs font-black uppercase tracking-wider translate-y-0 active:translate-y-1 transition-all">
                                    Book Chat
                                </Button>
                                <Button variant="outline" className="h-12 w-12 rounded-xl border-teal-100 text-teal-600 hover:bg-teal-50 p-0 shadow-sm">
                                    <Video className="h-5 w-5" />
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Why Consult Section */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-10">
                {[
                    { title: "Instant Chat", desc: "Get replies within 10 minutes", icon: MessageCircle, color: "text-blue-500", bg: "bg-blue-50" },
                    { title: "Digital Recipe", desc: "Receive formal treatment plans", icon: CheckCircle2, color: "text-green-500", bg: "bg-green-50" },
                    { title: "Available 24/7", desc: "Expert support always ready", icon: Clock, color: "text-orange-500", bg: "bg-orange-50" },
                ].map((item, i) => (
                    <div key={i} className="bg-white p-6 rounded-3xl flex items-center gap-5 shadow-sm">
                        <div className={`${item.bg} p-3 rounded-2xl`}>
                            <item.icon className={`h-6 w-6 ${item.color}`} />
                        </div>
                        <div>
                            <h4 className="font-black text-gray-900 text-sm tracking-tight">{item.title}</h4>
                            <p className="text-xs font-medium text-gray-400">{item.desc}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
