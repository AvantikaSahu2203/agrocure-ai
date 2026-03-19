import Link from "next/link"
import { Sprout } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Navbar() {
    return (
        <nav className="border-b bg-white">
            <div className="flex h-16 items-center px-4 md:px-6 container mx-auto">
                <Link className="flex items-center gap-2 font-semibold" href="/">
                    <Sprout className="h-6 w-6 text-green-600" />
                    <span className="text-xl font-bold text-gray-900">AgroCure AI</span>
                </Link>
                <div className="ml-auto flex gap-4">
                    <Link href="/login">
                        <Button variant="ghost">Login</Button>
                    </Link>
                    <Link href="/register">
                        <Button>Get Started</Button>
                    </Link>
                </div>
            </div>
        </nav>
    )
}
