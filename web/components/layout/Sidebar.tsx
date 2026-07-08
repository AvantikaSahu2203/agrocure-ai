'use client'

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { LayoutDashboard, Sprout, Store, UserCheck, ShieldAlert, LogOut, BarChart3, Lightbulb } from "lucide-react"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/context/LanguageContext"
import { Languages } from "lucide-react"

export function Sidebar() {
    const pathname = usePathname()
    const { lang, setLang, t } = useLanguage()

    const links = []

    if (pathname.includes("/admin")) {
        links.push(
            { href: "/admin", label: t('dashboard'), icon: LayoutDashboard },
            { href: "/admin/users", label: t('profile'), icon: UserCheck },
            { href: "/admin/reports", label: t('reports'), icon: ShieldAlert },
        )
    } else {
        // Default to Farmer
        links.push(
            { href: "/farmer", label: t('dashboard'), icon: LayoutDashboard },
            { href: "/farmer/crops", label: t('myCrops'), icon: Sprout },
            { href: "/farmer/disease-check", label: t('diseaseCheck'), icon: ShieldAlert },
            { href: "/farmer/stores", label: t('nearbyStores'), icon: Store },
            { href: "/farmer/reports", label: t('reports'), icon: BarChart3 },
            { href: "/farmer/advisory", label: t('smartAdvisory'), icon: Lightbulb },
            { href: "/farmer/profile", label: t('profile'), icon: UserCheck },
        )
    }

    const router = useRouter()

    const handleSignOut = () => {
        localStorage.removeItem('token')
        router.push('/login')
    }

    return (
        <div className="flex h-full flex-col border-r bg-gray-50/40 w-64 hidden md:flex">
            <div className="flex h-16 items-center border-b px-6 justify-between">
                <Link className="flex items-center gap-2 font-semibold" href="/">
                    <Sprout className="h-6 w-6 text-green-600" />
                    <span className="text-xl font-bold">AgroCure AI</span>
                </Link>
                {/* Language Toggle */}
                <button 
                  onClick={() => setLang(lang === 'en' ? 'hi' : 'en')}
                  className="p-2 hover:bg-green-50 rounded-full text-green-600 transition-colors"
                  title={t('selectLanguage')}
                >
                  <div className="flex flex-col items-center leading-none">
                    <Languages className="h-4 w-4 mb-0.5" />
                    <span className="text-[8px] font-bold">{lang.toUpperCase()}</span>
                  </div>
                </button>
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
                <button 
                    onClick={handleSignOut}
                    className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-500 hover:bg-red-50 transition-all"
                >
                    <LogOut className="h-4 w-4" />
                    {t('signOut')}
                </button>
            </div>
        </div>
    )
}
