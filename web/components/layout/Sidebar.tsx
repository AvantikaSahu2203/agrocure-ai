'use client'

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, Sprout, Store, UserCheck, ShieldAlert, LogOut, BarChart3, Lightbulb } from "lucide-react"
import { cn } from "@/lib/utils"

export function Sidebar() {
    const pathname = usePathname()

    const links = []

    if (pathname.includes("/admin")) {
        links.push(
            { href: "/admin", label: "Overview", icon: LayoutDashboard },
            { href: "/admin/users", label: "Users", icon: UserCheck },
            { href: "/admin/reports", label: "Reports", icon: ShieldAlert },
        )
    } else {
        // Default to Farmer
        links.push(
            { href: "/farmer", label: "Dashboard", icon: LayoutDashboard },
            { href: "/farmer/crops", label: "My Crops", icon: Sprout },
            { href: "/farmer/disease-check", label: "Disease Check", icon: ShieldAlert },
            { href: "/farmer/stores", label: "Nearby Stores", icon: Store },
            { href: "/farmer/reports", label: "Reports", icon: BarChart3 },
            { href: "/farmer/advisory", label: "Smart Advisory", icon: Lightbulb },
            { href: "/farmer/profile", label: "Profile", icon: UserCheck },
        )
    }

    return (
        <div className="flex h-full flex-col border-r bg-gray-50/40 w-64 hidden md:flex">
            <div className="flex h-16 items-center border-b px-6">
                <Link className="flex items-center gap-2 font-semibold" href="/">
                    <Sprout className="h-6 w-6 text-green-600" />
                    <span className="text-xl font-bold">AgroCure AI</span>
                </Link>
            </div>
            <div className="flex-1 overflow-auto py-2">
                <nav className="grid gap-1 px-4 text-sm font-medium">
                    {links.map((link) => {
                        const Icon = link.icon
                        return (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-green-600",
                                    pathname === link.href ? "bg-green-100 text-green-700" : "text-gray-500"
                                )}
                            >
                                <Icon className="h-4 w-4" />
                                {link.label}
                            </Link>
                        )
                    })}
                </nav>
            </div>
            <div className="border-t p-4">
                <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-500 hover:bg-red-50 transition-all">
                    <LogOut className="h-4 w-4" />
                    Sign Out
                </button>
            </div>
        </div>
    )
}
