'use client'

import { useState, useEffect } from "react"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "../../../../components/ui/badge"
import { Search, ShoppingCart, Filter, Plus } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import api from "@/lib/api"

interface Product {
    id: string
    quantity: number
    unit_price: number
    medicine: {
        name: string
        description: string
        image_url: string
        category: string
        manufacturer: string
    }
    store: {
        name: string
    }
}

export default function MarketPage() {
    const [products, setProducts] = useState<Product[]>([])
    const [searchTerm, setSearchTerm] = useState("")
    const [loading, setLoading] = useState(true)
    const [cartCount, setCartCount] = useState(0)
    const router = useRouter()

    useEffect(() => {
        fetchProducts()
        updateCartCount()
    }, [])

    const updateCartCount = () => {
        const cart = JSON.parse(localStorage.getItem("cart") || "[]")
        setCartCount(cart.length)
    }

    const fetchProducts = async () => {
        try {
            const res = await api.get("/market/products")
            setProducts(res.data)
        } catch (error) {
            console.error("Failed to fetch products", error)
        } finally {
            setLoading(false)
        }
    }

    const addToCart = (product: Product) => {
        const cart = JSON.parse(localStorage.getItem("cart") || "[]")
        cart.push(product)
        localStorage.setItem("cart", JSON.stringify(cart))
        updateCartCount()
        // Optional: Show toast
    }

    const filteredProducts = products.filter(p =>
        p.medicine?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.medicine?.category?.toLowerCase().includes(searchTerm.toLowerCase())
    )

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 border-l-4 border-purple-600 pl-3">AgroMarket</h1>
                    <p className="text-gray-500 text-sm pl-4 mt-1">Buy authentic medicines & fertilizers</p>
                </div>
                <Link href="/farmer/market/cart">
                    <Button className="relative bg-white text-gray-800 border-gray-200 hover:bg-gray-50 border shadow-sm">
                        <ShoppingCart className="h-5 w-5 mr-2" />
                        Cart
                        {cartCount > 0 && (
                            <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                                {cartCount}
                            </span>
                        )}
                    </Button>
                </Link>
            </div>

            {/* Search & Filter */}
            <div className="flex gap-3">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                    <Input
                        className="pl-10 h-12 rounded-xl border-gray-200 bg-white shadow-sm"
                        placeholder="Search for medicines, fertilizers..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Button variant="outline" className="h-12 rounded-xl bg-white border-gray-200 aspect-square p-0">
                    <Filter className="h-5 w-5 text-gray-500" />
                </Button>
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {loading ? (
                    <div className="col-span-full py-20 text-center text-gray-500">Loading products...</div>
                ) : filteredProducts.length > 0 ? (
                    filteredProducts.map((product) => (
                        <Card key={product.id} className="border-none shadow-sm hover:shadow-md transition-all rounded-2xl overflow-hidden group flex flex-col h-full bg-white">
                            <div className="h-48 bg-gray-100 relative overflow-hidden">
                                {product.medicine?.image_url ? (
                                    <img
                                        src={product.medicine.image_url}
                                        alt={product.medicine.name}
                                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-gray-300">No Image</div>
                                )}
                                <div className="absolute top-3 left-3">
                                    <Badge className="bg-white/90 text-gray-800 hover:bg-white backdrop-blur-sm">
                                        {product.medicine?.category || "General"}
                                    </Badge>
                                </div>
                            </div>

                            <CardContent className="p-4 flex-1">
                                <div className="mb-2">
                                    <h3 className="font-bold text-gray-900 line-clamp-1">{product.medicine?.name}</h3>
                                    <p className="text-xs text-gray-500">{product.medicine?.manufacturer}</p>
                                </div>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-lg font-bold text-green-700">₹{product.unit_price}</span>
                                    <span className="text-xs text-gray-400 font-normal">/ unit</span>
                                </div>
                                <p className="text-xs text-gray-400 mt-2 flex items-center">
                                    Sold by: <span className="text-gray-600 ml-1 font-medium">{product.store?.name}</span>
                                </p>
                            </CardContent>

                            <CardFooter className="p-4 pt-0">
                                <Button
                                    className="w-full bg-green-600 hover:bg-green-700 rounded-xl"
                                    onClick={() => addToCart(product)}
                                >
                                    <Plus className="h-4 w-4 mr-2" />
                                    Add to Cart
                                </Button>
                            </CardFooter>
                        </Card>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center text-gray-500">
                        No products found matching "{searchTerm}"
                    </div>
                )}
            </div>
        </div>
    )
}
