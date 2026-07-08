'use client'

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Sidebar } from "@/components/layout/Sidebar"

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const router = useRouter()
    const [isAuthenticated, setIsAuthenticated] = useState(false)

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (!token) {
            router.push('/login')
        } else {
            setIsAuthenticated(true)
        }
    }, [router])

    if (!isAuthenticated) {
        return <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <div className="animate-pulse text-green-700 font-bold italic tracking-widest">AGROCURE AI SECURE...</div>
        </div>
    }

    return (
        <div className="flex min-h-screen w-full">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                {/* Header could go here */}
                <header className="flex h-16 items-center gap-4 border-b bg-white px-6 md:hidden">
                    {/* Mobile Sidebar Trigger would go here */}
                    <span className="font-bold">AgroCure AI</span>
                </header>
                <main className="flex-1 p-4 md:p-6 overflow-y-auto bg-gray-50">
                    {children}
                </main>
            </div>
        </div>
    )
}
