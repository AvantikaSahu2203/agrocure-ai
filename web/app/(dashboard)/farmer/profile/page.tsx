'use client'

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { User, Mail, Shield, Calendar, Settings, Edit2, Camera, AlertTriangle, Activity, Phone, Save, X, Loader2 } from "lucide-react"
import api from "@/lib/api"

interface UserProfile {
    id: string
    email: string
    full_name: string
    phone_number: string | null
    role: string
    is_active: boolean
    created_at: string
}

export default function ProfilePage() {
    const router = useRouter()
    const [profile, setProfile] = useState<UserProfile | null>(null)
    const [loading, setLoading] = useState(true)
    const [errorType, setErrorType] = useState<'auth' | 'connection' | null>(null)
    const [isEditing, setIsEditing] = useState(false)
    const [formData, setFormData] = useState({
        full_name: "",
        phone_number: ""
    })
    const [saving, setSaving] = useState(false)

    async function fetchProfile() {
        try {
            const res = await api.get("/users/me")
            setProfile(res.data)
            setFormData({
                full_name: res.data.full_name || "",
                phone_number: res.data.phone_number || ""
            })
            setErrorType(null)
        } catch (error: any) {
            console.error("Failed to fetch profile", error)
            if (error.response?.status === 401 || error.response?.status === 403) {
                setErrorType('auth')
            } else {
                setErrorType('connection')
            }
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchProfile()
    }, [])

    const handleSave = async () => {
        setSaving(true)
        try {
            const res = await api.patch("/users/me", formData)
            setProfile(res.data)
            setIsEditing(false)
            // Show simple success (ideally use toast)
            alert("Profile updated successfully!")
        } catch (error) {
            console.error("Failed to update profile", error)
            alert("Failed to update profile. Please try again.")
        } finally {
            setSaving(false)
        }
    }

    if (loading) {
        return (
            <div className="flex-1 bg-gray-50 min-h-screen flex items-center justify-center">
                <Loader2 className="h-12 w-12 text-green-700 animate-spin" />
            </div>
        )
    }

    if (errorType === 'auth' || !profile) {
        return (
            <div className="flex-1 bg-gray-50 min-h-screen flex items-center justify-center p-8">
                <Card className="max-w-md w-full rounded-3xl border-none shadow-2xl p-8 text-center bg-white">
                    <div className={`${errorType === 'auth' ? 'bg-amber-50' : 'bg-red-50'} h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-6`}>
                        {errorType === 'auth' ? (
                            <User className="h-8 w-8 text-amber-500" />
                        ) : (
                            <AlertTriangle className="h-8 w-8 text-red-500" />
                        )}
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        {errorType === 'auth' ? "Login Required" : "Connection Issues"}
                    </h2>
                    <p className="text-gray-500 mb-6">
                        {errorType === 'auth'
                            ? "You need to be logged in to view your profile. Please sign in to your account."
                            : "We couldn't reach the profile server. Please check your connection and try again."}
                    </p>
                    {errorType === 'auth' ? (
                        <Button onClick={() => router.push("/login")} className="w-full rounded-2xl bg-amber-600 hover:bg-amber-700 h-12">
                            Go to Login
                        </Button>
                    ) : (
                        <Button onClick={() => fetchProfile()} className="w-full rounded-2xl bg-green-700 hover:bg-green-800 h-12">
                            Try Again
                        </Button>
                    )}
                </Card>
            </div>
        )
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 space-y-6 max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-l-4 border-green-700 pl-4 py-1">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
                    <p className="text-gray-500 text-sm mt-1">Manage your account settings and preferences</p>
                </div>
                {!isEditing ? (
                    <Button
                        onClick={() => setIsEditing(true)}
                        className="rounded-full shadow-lg h-11 px-6 bg-green-700 hover:bg-green-800 transition-all transform hover:scale-105"
                    >
                        <Edit2 className="h-4 w-4 mr-2" />
                        Edit Profile
                    </Button>
                ) : (
                    <div className="flex gap-2">
                        <Button
                            onClick={() => setIsEditing(false)}
                            variant="outline"
                            className="rounded-full h-11 px-6 border-gray-200"
                        >
                            <X className="h-4 w-4 mr-2" />
                            Cancel
                        </Button>
                        <Button
                            onClick={handleSave}
                            disabled={saving}
                            className="rounded-full shadow-lg h-11 px-6 bg-green-700 hover:bg-green-800 transition-all transform hover:scale-105"
                        >
                            {saving ? (
                                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            ) : (
                                <Save className="h-4 w-4 mr-2" />
                            )}
                            Save Changes
                        </Button>
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Profile Card */}
                <Card className="lg:col-span-1 rounded-3xl border-none shadow-xl overflow-hidden bg-white">
                    <div className="h-24 bg-gradient-to-r from-green-600 to-emerald-700 w-full" />
                    <CardContent className="pt-0 -mt-12 text-center relative z-10 px-6 pb-8">
                        <div className="relative inline-block group">
                            <Avatar className="h-24 w-24 border-4 border-white shadow-lg mx-auto bg-white cursor-pointer transition-transform group-hover:scale-110">
                                <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${profile.full_name || profile.email}`} />
                                <AvatarFallback>{(profile.full_name || profile.email).charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div className="absolute bottom-0 right-0 bg-white p-1.5 rounded-full shadow-md border animate-bounce group-hover:animate-none">
                                <Camera className="h-3.5 w-3.5 text-green-700" />
                            </div>
                        </div>
                        <h2 className="text-xl font-bold mt-4 text-gray-900">{profile.full_name || "New Farmer"}</h2>
                        <Badge variant="secondary" className="mt-2 bg-green-50 text-green-700 border-green-200 capitalize px-3">
                            {profile.role || "Farmer"}
                        </Badge>
                        <div className="mt-6 flex flex-col gap-3 text-left">
                            <div className="flex items-center gap-3 text-sm text-gray-600 p-2 hover:bg-gray-50 rounded-xl transition-colors">
                                <div className="bg-green-100 p-2 rounded-lg">
                                    <Mail className="h-4 w-4 text-green-700" />
                                </div>
                                <span className="truncate">{profile.email}</span>
                            </div>
                            <div className="flex items-center gap-3 text-sm text-gray-600 p-2 hover:bg-gray-50 rounded-xl transition-colors">
                                <div className="bg-green-100 p-2 rounded-lg">
                                    <Shield className="h-4 w-4 text-green-700" />
                                </div>
                                <span>{profile.is_active ? "Account Active" : "Account Suspended"}</span>
                            </div>
                            <div className="flex items-center gap-3 text-sm text-gray-600 p-2 hover:bg-gray-50 rounded-xl transition-colors">
                                <div className="bg-green-100 p-2 rounded-lg">
                                    <Calendar className="h-4 w-4 text-green-700" />
                                </div>
                                <span>Joined {profile.created_at ? new Date(profile.created_at).toLocaleDateString(undefined, { month: 'long', year: 'numeric' }) : "Recently"}</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Settings & Info */}
                <div className="lg:col-span-2 space-y-6">
                    <Card className="rounded-3xl border-none shadow-xl bg-white overflow-hidden">
                        <CardHeader className="bg-gray-50/50 border-b border-gray-100 pb-4">
                            <CardTitle className="text-lg flex items-center gap-2 text-gray-800">
                                <User className="h-5 w-5 text-green-700" />
                                Personal Information
                            </CardTitle>
                            <CardDescription>Update your personal details here</CardDescription>
                        </CardHeader>
                        <CardContent className="p-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-sm font-semibold text-gray-700">Full Name</Label>
                                    {isEditing ? (
                                        <Input
                                            value={formData.full_name}
                                            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                            className="rounded-xl border-gray-200"
                                            placeholder="Enter your full name"
                                        />
                                    ) : (
                                        <div className="p-3 bg-gray-50 rounded-2xl border-none text-gray-900 font-medium">
                                            {profile.full_name || "Not set"}
                                        </div>
                                    )}
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-sm font-semibold text-gray-700">Phone Number</Label>
                                    {isEditing ? (
                                        <Input
                                            value={formData.phone_number}
                                            onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                                            className="rounded-xl border-gray-200"
                                            placeholder="Enter your phone number"
                                        />
                                    ) : (
                                        <div className="p-3 bg-gray-50 rounded-2xl border-none text-gray-900 font-medium">
                                            {profile.phone_number || "Not set"}
                                        </div>
                                    )}
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-sm font-semibold text-gray-700">Email Address</Label>
                                    <div className="p-3 bg-gray-50 rounded-2xl border-none text-gray-500 font-medium lowercase">
                                        {profile.email}
                                    </div>
                                    <p className="text-[10px] text-gray-400 mt-1 italic">* Email cannot be changed</p>
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-sm font-semibold text-gray-700">Account Type</Label>
                                    <div className="p-3 bg-gray-50 rounded-2xl border-none text-gray-900 font-medium capitalize">
                                        {profile.role}
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="rounded-3xl border-none shadow-xl bg-white">
                        <CardHeader>
                            <CardTitle className="text-lg flex items-center gap-2 text-gray-800">
                                <Settings className="h-5 w-5 text-green-700" />
                                Dashboard Preferences
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-2xl transition-colors cursor-pointer group">
                                <div className="flex items-center gap-3">
                                    <div className="h-2 w-2 rounded-full bg-green-500 group-hover:scale-150 transition-transform"></div>
                                    <span className="text-sm font-medium text-gray-700">Email Notifications</span>
                                </div>
                                <span className="text-xs text-gray-400 font-bold italic">COMING SOON</span>
                            </div>
                            <div className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-2xl transition-colors cursor-pointer group">
                                <div className="flex items-center gap-3">
                                    <div className="h-2 w-2 rounded-full bg-blue-400 group-hover:scale-150 transition-transform"></div>
                                    <span className="text-sm font-medium text-gray-700">Push Notifications</span>
                                </div>
                                <span className="text-xs text-gray-400 font-bold italic">COMING SOON</span>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
