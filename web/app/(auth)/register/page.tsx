'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Sprout } from "lucide-react"
import api from '@/lib/api'

export default function RegisterPage() {
    const router = useRouter()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [fullName, setFullName] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            // 1. Create User
            await api.post('/users/', {
                email,
                password,
                full_name: fullName,
            });

            // 2. Automatically Log In
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);

            const loginRes = await api.post('/login/access-token', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            if (loginRes.data.access_token) {
                localStorage.setItem('token', loginRes.data.access_token);
                localStorage.setItem('user_email', email);
                router.push('/farmer');
            } else {
                setError('Registration successful but login failed. Please sign in manually.');
            }
        } catch (err: any) {
            console.error('Registration/Login error:', err);
            setError(err.response?.data?.detail || 'An error occurred during registration. Please try again.');
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
            <div className="w-full max-w-md space-y-8 bg-white p-8 rounded-lg shadow">
                <div className="flex flex-col items-center">
                    <Link className="flex items-center gap-2 font-semibold mb-6" href="/">
                        <Sprout className="h-8 w-8 text-green-600" />
                        <span className="text-2xl font-bold text-gray-900">AgroCure AI</span>
                    </Link>
                    <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                        Create your account
                    </h2>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="-space-y-px rounded-md shadow-sm">
                        <div>
                            <input
                                id="full-name"
                                name="fullName"
                                type="text"
                                autoComplete="name"
                                required
                                className="relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-green-600 sm:text-sm sm:leading-6 px-3"
                                placeholder="Full Name"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                            />
                        </div>
                        <div>
                            <input
                                id="email-address"
                                name="email"
                                type="email"
                                autoComplete="email"
                                required
                                className="relative block w-full border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-green-600 sm:text-sm sm:leading-6 px-3"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="new-password"
                                required
                                className="relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-green-600 sm:text-sm sm:leading-6 px-3"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && <div className="text-red-500 text-sm text-center">{error}</div>}

                    <div>
                        <Button
                            type="submit"
                            className="group relative flex w-full justify-center"
                            disabled={loading}
                        >
                            {loading ? 'Creating Account...' : 'Sign up'}
                        </Button>
                    </div>

                    <div className="text-sm text-center">
                        <Link href="/login" className="font-medium text-green-600 hover:text-green-500">
                            Already have an account? Sign in
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    )
}
