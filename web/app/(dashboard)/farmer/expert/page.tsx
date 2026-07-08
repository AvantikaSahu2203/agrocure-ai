'use client'

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
    Mic, 
    Image as ImageIcon, 
    Send, 
    CheckCircle2, 
    AlertCircle, 
    Trash2, 
    ShieldCheck, 
    MessageSquare,
    Loader2
} from "lucide-react"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { db, storage } from "@/lib/firebase"
import { collection, addDoc } from "firebase/firestore"
import { ref, uploadBytes, getDownloadURL } from "firebase/storage"
import { useLanguage } from "@/context/LanguageContext"

export default function FarmerSupportPage() {
    const { lang } = useLanguage();
    const isHindi = lang === 'hi';

    // State
    const [name, setName] = useState("")
    const [message, setMessage] = useState("")
    const [image, setImage] = useState<File | null>(null)
    const [imagePreview, setImagePreview] = useState<string | null>(null)
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
    const [isRecording, setIsRecording] = useState(false)
    const [submitting, setSubmitting] = useState(false)
    const [recordTime, setRecordTime] = useState(0)
    
    // Refs for MediaRecorder
    const mediaRecorderRef = useRef<MediaRecorder | null>(null)
    const audioChunksRef = useRef<Blob[]>([])
    const timerRef = useRef<NodeJS.Timeout | null>(null)

    // Handlers
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            const mediaRecorder = new MediaRecorder(stream)
            mediaRecorderRef.current = mediaRecorder
            audioChunksRef.current = []

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data)
                }
            }

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
                setAudioBlob(audioBlob)
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorder.start()
            setIsRecording(true)
            setRecordTime(0)
            timerRef.current = setInterval(() => {
                setRecordTime(prev => {
                    if (prev >= 30) {
                        stopRecording()
                        return 30
                    }
                    return prev + 1
                })
            }, 1000)
        } catch (err) {
            console.error("Microphone access denied", err)
            alert(isHindi ? "माइक एक्सेस नहीं मिला" : "Microphone access denied")
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)
            if (timerRef.current) clearInterval(timerRef.current)
        }
    }

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            setImage(file)
            setImagePreview(URL.createObjectURL(file))
        }
    }

    const handleSubmit = async () => {
        if (!name || (!message && !image && !audioBlob)) {
            alert(isHindi ? "कृपया जानकारी पूरी भरें" : "Please complete the required information")
            return
        }

        setSubmitting(true)

        try {
            let imageUrl = null
            let audioUrl = null

            // 1. Upload Assets
            if (image) {
                const imageRef = ref(storage, `images/${Date.now()}_${image.name}`)
                await uploadBytes(imageRef, image)
                imageUrl = await getDownloadURL(imageRef)
            }

            if (audioBlob) {
                const audioRef = ref(storage, `audio/${Date.now()}.wav`)
                await uploadBytes(audioRef, audioBlob)
                audioUrl = await getDownloadURL(audioRef)
            }

            // 2. Save to Firestore
            await addDoc(collection(db, "complaints"), {
                name,
                message,
                imageUrl,
                audioUrl,
                timestamp: Date.now(),
                status: "pending",
                source: "web"
            })

            alert(isHindi ? "सफल! आपकी विशेषज्ञ सलाह दर्ज की गई है।" : "Success! Your request has been sent.")
            
            // CC to local storage for user record
            const localHistory = JSON.parse(localStorage.getItem('expert_consults') || '[]')
            localHistory.push({ name, timestamp: Date.now(), status: 'pending', message })
            localStorage.setItem('expert_consults', JSON.stringify(localHistory))

            // Reset
            resetForm()
        } catch (error) {
            console.error(error)
            alert(isHindi ? "दर्ज करने में विफल। कृपया फिर से प्रयास करें।" : "Submission failed. Please try again.")
        } finally {
            setSubmitting(false)
        }
    }

    const resetForm = () => {
        setName("")
        setMessage("")
        setImage(null)
        setImagePreview(null)
        setAudioBlob(null)
        setRecordTime(0)
    }

    return (
        <div className="flex-1 bg-[#f8fafc] min-h-screen p-4 md:p-10 max-w-5xl mx-auto space-y-8">
            {/* Unified Support Header */}
            <div className="bg-white rounded-[40px] p-8 md:p-12 shadow-2xl shadow-emerald-500/5 border border-emerald-50 relative overflow-hidden">
                <div className="relative z-10 space-y-4">
                    <Badge className="bg-emerald-100 text-emerald-700 hover:bg-emerald-100 border-none px-4 py-1.5 rounded-full uppercase text-[10px] font-black tracking-widest">
                        {isHindi ? "पूर्ण ऑनलाइन सहायता" : "Complete Online Support"}
                    </Badge>
                    <h1 className="text-3xl md:text-5xl font-black text-slate-900 leading-tight tracking-tight">
                        {isHindi ? "विशेषज्ञ से " : "Consult with "}<span className="text-emerald-600 font-extrabold">{isHindi ? "बात करें" : "Agro Experts"}</span>
                    </h1>
                    <p className="text-slate-500 font-medium max-w-xl text-lg">
                        {isHindi 
                          ? "अपनी समस्या बोलकर, लिखकर या फोटो भेजकर हमें बताएं। हमारे डॉक्टर जल्द ही जवाब देंगे।" 
                          : "Tell us about your crop issues via text, voice, or image. Our certified doctors will respond shortly."}
                    </p>
                </div>
                <div className="absolute -top-10 -right-10 w-64 h-64 bg-emerald-50 rounded-full blur-3xl opacity-60" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Form */}
                <Card className="lg:col-span-2 rounded-[40px] border-none shadow-2xl bg-white overflow-hidden p-8 md:p-10">
                    <div className="space-y-8">
                        {/* Name Input */}
                        <div className="space-y-3">
                            <label className="text-xs font-black uppercase text-slate-400 tracking-wider">
                                {isHindi ? "आपका पूरा नाम" : "Your Full Name"}
                            </label>
                            <Input 
                                placeholder={isHindi ? "यहाँ लिखें..." : "Enter your name..."}
                                className="h-16 rounded-2xl bg-slate-50 border-emerald-50 focus-visible:ring-emerald-600 font-bold text-lg px-6"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                        </div>

                        {/* Messagebox */}
                        <div className="space-y-3">
                            <label className="text-xs font-black uppercase text-slate-400 tracking-wider">
                                {isHindi ? "समस्या का विवरण (वैकल्पिक)" : "Problem Details (Optional)"}
                            </label>
                            <Textarea 
                                placeholder={isHindi ? "यहाँ अपनी समस्या लिखें..." : "Describe what is happening to your crop..."}
                                className="min-h-[160px] rounded-3xl bg-slate-50 border-emerald-50 focus-visible:ring-emerald-600 font-medium text-lg p-6 resize-none"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            />
                        </div>

                        {/* Multimodal Inputs */}
                        <div className="flex flex-col md:flex-row gap-6">
                            {/* Voice Control */}
                            <div className={`flex-1 p-6 rounded-[32px] border-2 border-dashed transition-all flex flex-col items-center justify-center gap-4 ${isRecording ? 'bg-red-50 border-red-200' : 'bg-emerald-50/30 border-emerald-100'}`}>
                                <h4 className="text-sm font-black text-slate-700 uppercase">{isHindi ? "आवाज़ भेजें" : "Voice Message"}</h4>
                                <Button 
                                    onClick={isRecording ? stopRecording : startRecording}
                                    className={`h-20 w-20 rounded-full shadow-xl transition-transform active:scale-95 ${isRecording ? 'bg-red-500 hover:bg-red-600 shadow-red-500/30' : 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-500/30'}`}
                                >
                                    {isRecording ? <div className="h-6 w-6 bg-white rounded-sm animate-pulse" /> : <Mic className="h-8 w-8 text-white" />}
                                </Button>
                                <span className={`text-[10px] font-black uppercase tracking-widest ${isRecording ? 'text-red-500 animate-pulse' : 'text-slate-400'}`}>
                                    {isRecording ? `${recordTime}s / 30s` : (audioBlob ? (isHindi ? "आवाज़ चुनी गई" : "Voice Captured") : (isHindi ? "रिकॉर्ड शुरू करें" : "Start Recording"))}
                                </span>
                            </div>

                            {/* Image Picker */}
                            <div className="flex-1 p-6 rounded-[32px] border-2 border-dashed bg-blue-50/30 border-blue-100 transition-all flex flex-col items-center justify-center gap-4">
                                <h4 className="text-sm font-black text-slate-700 uppercase">{isHindi ? "फोटो जोड़ें" : "Upload Image"}</h4>
                                <label className="h-20 w-20 rounded-full bg-blue-600 hover:bg-blue-700 shadow-xl shadow-blue-500/30 flex items-center justify-center cursor-pointer transition-transform active:scale-95 leading-none">
                                    <ImageIcon className="h-8 w-8 text-white" />
                                    <input type="file" accept="image/*" className="hidden" onChange={handleImageChange} />
                                </label>
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">
                                    {image ? (isHindi ? "फोटो जोड़ी गई" : "Image Selected") : (isHindi ? "फोटो चुनें" : "Select Image")}
                                </span>
                            </div>
                        </div>

                        {/* Image Preview Area */}
                        {imagePreview && (
                            <div className="relative w-48 h-48 rounded-[32px] overflow-hidden border-4 border-white shadow-xl">
                                <img src={imagePreview} className="w-full h-full object-cover" alt="Preview" />
                                <button className="absolute top-3 right-3 bg-red-500 p-2 rounded-full text-white shadow-lg" onClick={() => {setImage(null); setImagePreview(null)}}>
                                    <Trash2 className="h-4 w-4" />
                                </button>
                            </div>
                        )}

                        {/* Submit Action */}
                        <Button 
                            disabled={submitting}
                            onClick={handleSubmit}
                            className="w-full h-20 rounded-[32px] bg-gradient-to-r from-emerald-600 to-emerald-800 hover:from-emerald-700 hover:to-emerald-900 shadow-2xl shadow-emerald-600/30 text-xl font-black uppercase tracking-widest translate-y-0 active:translate-y-2 transition-all mt-6"
                        >
                            {submitting ? (
                                <Loader2 className="h-10 w-10 animate-spin text-white" />
                            ) : (
                                <div className="flex items-center gap-4">
                                    <Send className="h-6 w-6" />
                                    {isHindi ? "सलाह भेजें" : "Submit Request"}
                                </div>
                            )}
                        </Button>
                    </div>
                </Card>

                {/* Info Sidebar */}
                <div className="space-y-6">
                    <Card className="rounded-[40px] border-none shadow-xl bg-emerald-900 text-white p-8">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="h-12 w-12 rounded-2xl bg-white/20 flex items-center justify-center">
                                <ShieldCheck className="h-6 w-6 text-white" />
                            </div>
                            <h4 className="text-xl font-black">{isHindi ? "सुरक्षित है" : "Safe & Secure"}</h4>
                        </div>
                        <p className="text-emerald-100/70 font-medium leading-relaxed">
                            {isHindi ? "आपकी तस्वीरें और आवाज़ सीधे हमारे डेटाबेस में जाती हैं। विशेषज्ञ इन्हें 24 घंटे के अंदर पढ़ेंगे।" 
                                     : "Your data is uploaded directly to our secure database. A certified expert will review it within 24 hours."}
                        </p>
                    </Card>

                    <div className="space-y-4">
                        {[
                            { title: isHindi ? "त्वरित जवाब" : "Quick Response", desc: isHindi ? "10 मिनट के अंदर" : "Within 10 mins", icon: MessageSquare, color: "text-blue-500", bg: "bg-blue-50" },
                            { title: isHindi ? "विशेषज्ञ डॉक्टर" : "Expert Doctors", desc: isHindi ? "प्रमाणित वैज्ञानिक" : "Certified Scientists", icon: CheckCircle2, color: "text-green-500", bg: "bg-green-50" },
                            { title: isHindi ? "सटीक इलाज" : "Accurate Cure", desc: isHindi ? "बीमारी का समाधान" : "Targeted diagnostics", icon: AlertCircle, color: "text-orange-500", bg: "bg-orange-50" },
                        ].map((item, i) => (
                            <div key={i} className="bg-white p-6 rounded-[28px] flex items-center gap-5 shadow-sm border border-slate-100 hover:border-emerald-100 transition-colors">
                                <div className={`${item.bg} p-4 rounded-2xl`}>
                                    <item.icon className={`h-6 w-6 ${item.color}`} />
                                </div>
                                <div className="space-y-0.5">
                                    <h5 className="font-black text-slate-900 text-sm tracking-tight leading-none">{item.title}</h5>
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">{item.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
