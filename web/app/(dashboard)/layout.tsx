import { Sidebar } from "@/components/layout/Sidebar"

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
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
