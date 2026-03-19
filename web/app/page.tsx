import Link from "next/link"
import { ArrowRight, CheckCircle, Leaf, ShieldCheck, Smartphone } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Navbar } from "@/components/layout/Navbar"

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {/* Hero Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-green-50">
          <div className="container px-4 md:px-6 mx-auto">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none text-green-900">
                  Healthy Crops, Wealthy Farmers
                </h1>
                <p className="mx-auto max-w-[700px] text-gray-600 md:text-xl">
                  Detect crop diseases instantly with AI using just your smartphone.
                  Connect with experts and verify medicine authenticity.
                </p>
              </div>
              <div className="space-x-4">
                <Link href="/register">
                  <Button size="lg" className="h-11 px-8">
                    Start Detecting Now <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Link href="/about">
                  <Button variant="outline" size="lg" className="h-11 px-8 bg-white">
                    Learn More
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-white">
          <div className="container px-4 md:px-6 mx-auto">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-gray-900">Key Features</h2>
            <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-3">
              <div className="flex flex-col items-center space-y-2 border-gray-200 p-4 rounded-lg">
                <div className="p-3 bg-green-100 rounded-full">
                  <Leaf className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">AI Disease Detection</h3>
                <p className="text-sm text-gray-500 text-center">
                  Identify crop diseases with over 95% accuracy by simply taking a photo.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-2 border-gray-200 p-4 rounded-lg">
                <div className="p-3 bg-blue-100 rounded-full">
                  <Smartphone className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Mobile First</h3>
                <p className="text-sm text-gray-500 text-center">
                  Designed for farmers on the go. Works offline and syncs when online.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-2 border-gray-200 p-4 rounded-lg">
                <div className="p-3 bg-yellow-100 rounded-full">
                  <ShieldCheck className="h-8 w-8 text-yellow-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Safe Products</h3>
                <p className="text-sm text-gray-500 text-center">
                  Verify the authenticity of fertilizers and pesticides from trusted stores.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-white">
        <p className="text-xs text-gray-500">© 2024 AgroCure AI. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4 text-gray-500" href="#">Terms of Service</Link>
          <Link className="text-xs hover:underline underline-offset-4 text-gray-500" href="#">Privacy</Link>
        </nav>
      </footer>
    </div>
  )
}
