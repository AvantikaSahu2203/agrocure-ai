'use client'

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Trash2, ArrowLeft, ShieldCheck } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function CartPage() {
    const [cart, setCart] = useState<any[]>([])
    const router = useRouter()

    useEffect(() => {
        const savedCart = JSON.parse(localStorage.getItem("cart") || "[]")
        setCart(savedCart)
    }, [])

    const removeFromCart = (index: number) => {
        const newCart = [...cart]
        newCart.splice(index, 1)
        setCart(newCart)
        localStorage.setItem("cart", JSON.stringify(newCart))
    }

    const calculateTotal = () => {
        return cart.reduce((total, item) => total + item.unit_price, 0)
    }

    const handleCheckout = () => {
        alert("Proceeding to Payment Gateway (Mock)... Order Placed!")
        localStorage.removeItem("cart")
        setCart([])
        router.push('/farmer/market')
    }

    return (
        <div className="flex-1 bg-gray-50 min-h-screen p-4 md:p-8 max-w-4xl mx-auto">
            <div className="flex items-center gap-4 mb-8">
                <Link href="/farmer/market">
                    <Button variant="ghost" className="p-0 h-auto hover:bg-transparent">
                        <ArrowLeft className="h-6 w-6 text-gray-600" />
                    </Button>
                </Link>
                <h1 className="text-2xl font-bold text-gray-900">Your Cart ({cart.length})</h1>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
                {/* Cart Items */}
                <div className="md:col-span-2 space-y-4">
                    {cart.length > 0 ? (
                        cart.map((item, index) => (
                            <Card key={index} className="border-none shadow-sm rounded-xl">
                                <CardContent className="p-4 flex gap-4">
                                    <div className="h-20 w-20 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                                        <img src={item.medicine?.image_url} alt="" className="h-full w-full object-cover" />
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <h3 className="font-bold text-gray-900">{item.medicine?.name}</h3>
                                                <p className="text-sm text-gray-500">{item.medicine?.manufacturer}</p>
                                            </div>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="text-red-500 hover:text-red-600 hover:bg-red-50 pr-0"
                                                onClick={() => removeFromCart(index)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                        <div className="mt-2 font-bold text-green-700">
                                            ₹{item.unit_price}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    ) : (
                        <div className="text-center py-20 bg-white rounded-xl shadow-sm">
                            <p className="text-gray-500">Your cart is empty.</p>
                            <Link href="/farmer/market">
                                <Button variant="link" className="text-green-600">Browse Products</Button>
                            </Link>
                        </div>
                    )}
                </div>

                {/* Summary */}
                <div className="md:col-span-1">
                    <Card className="border-none shadow-sm rounded-xl sticky top-4">
                        <CardContent className="p-6">
                            <h3 className="font-bold text-lg mb-4">Order Summary</h3>
                            <div className="space-y-3 mb-6">
                                <div className="flex justify-between text-gray-600">
                                    <span>Subtotal</span>
                                    <span>₹{calculateTotal().toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between text-gray-600">
                                    <span>Delivery Fee</span>
                                    <span className="text-green-600">Free</span>
                                </div>
                                <div className="border-t pt-3 flex justify-between font-bold text-lg">
                                    <span>Total</span>
                                    <span>₹{calculateTotal().toFixed(2)}</span>
                                </div>
                            </div>

                            <Button
                                className="w-full bg-green-600 hover:bg-green-700 h-12 rounded-xl text-base"
                                disabled={cart.length === 0}
                                onClick={handleCheckout}
                            >
                                Proceed to Checkout
                            </Button>

                            <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-400">
                                <ShieldCheck className="h-4 w-4" />
                                Secure Payment
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
