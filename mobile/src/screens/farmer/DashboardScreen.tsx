import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, ImageBackground } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { 
    Cloud, 
    Bell, 
    Camera, 
    BookOpen, 
    ShoppingCart, 
    MapPin, 
    BarChart3, 
    MessageCircle, 
    ChevronRight, 
    Leaf,
    Lightbulb,
    Thermometer,
    Droplets
} from 'lucide-react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../types/navigation';
import { COLORS, SHADOWS } from '../../theme/theme';

export default function DashboardScreen() {
    const navigation = useNavigation<StackNavigationProp<RootStackParamList>>();

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header */}
            <View className="bg-white px-6 py-4 flex-row items-center justify-between border-b border-gray-100">
                <View className="flex-row items-center gap-2">
                    <View className="bg-green-700 p-2 rounded-xl">
                        <Leaf color="white" size={20} fill="white" />
                    </View>
                    <Text className="font-bold text-xl text-gray-900">AgroCure AI</Text>
                </View>
                <View className="flex-row items-center gap-3">
                    <TouchableOpacity className="bg-gray-100 p-2 rounded-full">
                        <Bell color="#4b5563" size={20} />
                        <View className="absolute top-2 right-2 h-2.5 w-2.5 bg-red-500 rounded-full border-2 border-white" />
                    </TouchableOpacity>
                </View>
            </View>

            <ScrollView className="flex-1" showsVerticalScrollIndicator={false} contentContainerStyle={{ padding: 20, paddingBottom: 40 }}>
                {/* Hero Section */}
                <View className="rounded-3xl bg-green-800 p-6 mb-6 overflow-hidden relative" style={SHADOWS.md}>
                    <View className="z-10">
                        <Text className="text-white text-2xl font-bold mb-1">Protect Your Crops</Text>
                        <Text className="text-green-100 opacity-80 mb-4 text-sm">Scan, detect, and cure instantly</Text>
                        <TouchableOpacity 
                            className="bg-white px-6 py-3 rounded-xl self-start"
                            onPress={() => navigation.navigate('Scan' as any)}
                        >
                            <Text className="text-green-800 font-bold">Start Scanning</Text>
                        </TouchableOpacity>
                    </View>
                    <View className="absolute -bottom-4 -right-4 bg-green-700 w-32 h-32 rounded-full opacity-30" />
                    <View className="absolute top-2 -right-8 bg-green-600 w-24 h-24 rounded-full opacity-20" />
                </View>

                {/* Weather Card */}
                <View className="bg-white p-5 rounded-3xl mb-6 flex-row items-center justify-between border border-gray-100" style={SHADOWS.sm}>
                    <View className="flex-row items-center gap-4">
                        <View className="bg-yellow-100 p-3 rounded-full">
                            <Cloud color="#ca8a04" size={28} fill="#ca8a04" />
                        </View>
                        <View>
                            <View className="flex-row items-baseline gap-2">
                                <Text className="text-2xl font-bold text-gray-900">32°C</Text>
                                <Text className="text-gray-400 text-xs">— Partly Cloudy</Text>
                            </View>
                            <View className="flex-row gap-3 mt-1">
                                <View className="flex-row items-center gap-1">
                                    <Droplets color="gray" size={12} />
                                    <Text className="text-gray-400 text-[10px]">68% Hum.</Text>
                                </View>
                                <View className="flex-row items-center gap-1">
                                    <Thermometer color="gray" size={12} />
                                    <Text className="text-gray-400 text-[10px]">Low Risk</Text>
                                </View>
                            </View>
                        </View>
                    </View>
                    <ChevronRight color="#d1d5db" size={20} />
                </View>

                {/* Quick Actions Grid */}
                <Text className="text-lg font-bold text-gray-800 mb-4">Quick Actions</Text>
                <View className="flex-row flex-wrap gap-4 mb-6">
                    <TouchableOpacity 
                        className="w-[47%] bg-green-800 p-5 rounded-3xl h-32 justify-between"
                        onPress={() => navigation.navigate('Scan' as any)}
                    >
                        <View className="bg-white/20 w-10 h-10 rounded-xl items-center justify-center">
                            <Camera color="white" size={20} />
                        </View>
                        <View>
                            <Text className="text-white font-bold">Scan Disease</Text>
                            <Text className="text-green-200 text-[10px]">AI Detection</Text>
                        </View>
                    </TouchableOpacity>

                    <TouchableOpacity className="w-[47%] bg-white p-5 rounded-3xl h-32 justify-between border border-gray-100" style={SHADOWS.sm}>
                        <View className="bg-blue-100 w-10 h-10 rounded-xl items-center justify-center">
                            <BookOpen color="#2563eb" size={20} />
                        </View>
                        <View>
                            <Text className="text-gray-800 font-bold">Disease Library</Text>
                            <Text className="text-gray-400 text-[10px]">Browse all</Text>
                        </View>
                    </TouchableOpacity>

                    <TouchableOpacity className="w-[47%] bg-white p-5 rounded-3xl h-32 justify-between border border-gray-100" style={SHADOWS.sm}>
                        <View className="bg-purple-100 w-10 h-10 rounded-xl items-center justify-center">
                            <ShoppingCart color="#9333ea" size={20} />
                        </View>
                        <View>
                            <Text className="text-gray-800 font-bold">Market</Text>
                            <Text className="text-gray-400 text-[10px]">Buy medicine</Text>
                        </View>
                    </TouchableOpacity>

                    <TouchableOpacity className="w-[47%] bg-indigo-50 p-5 rounded-3xl h-32 justify-between border border-indigo-100" style={SHADOWS.sm}>
                        <View className="bg-indigo-600 w-10 h-10 rounded-xl items-center justify-center">
                            <Lightbulb color="white" size={20} />
                        </View>
                        <View>
                            <Text className="text-gray-900 font-bold">Advisory</Text>
                            <Text className="text-indigo-600 text-[10px] uppercase font-black">AI Powered</Text>
                        </View>
                    </TouchableOpacity>
                </View>

                {/* Recent Scans */}
                <View className="flex-row justify-between items-center mb-4">
                    <Text className="text-lg font-bold text-gray-800">Recent Scans</Text>
                    <TouchableOpacity>
                        <Text className="text-green-600 font-bold text-sm">See All</Text>
                    </TouchableOpacity>
                </View>

                <View className="space-y-3">
                    <View className="bg-white p-4 rounded-2xl flex-row items-center justify-between border border-gray-50" style={SHADOWS.sm}>
                        <View className="flex-row items-center gap-4">
                            <View className="bg-red-50 p-3 rounded-xl border border-red-100">
                                <View className="h-6 w-6 rounded-full bg-red-500/20 items-center justify-center">
                                    <View className="h-4 w-4 rounded-full bg-red-500" />
                                </View>
                            </View>
                            <View>
                                <Text className="font-bold text-gray-900">Tomato</Text>
                                <Text className="text-gray-500 text-xs">Early Blight</Text>
                            </View>
                        </View>
                        <View className="items-end">
                            <View className="bg-red-100 px-2 py-1 rounded-full">
                                <Text className="text-red-600 text-[8px] font-black uppercase">High Risk</Text>
                            </View>
                            <Text className="text-gray-400 text-[10px] mt-1">2h ago</Text>
                        </View>
                    </View>

                    <View className="bg-white p-4 rounded-2xl flex-row items-center justify-between border border-gray-50" style={SHADOWS.sm}>
                        <View className="flex-row items-center gap-4">
                            <View className="bg-green-50 p-3 rounded-xl border border-green-100">
                                <Leaf color="#16a34a" size={24} />
                            </View>
                            <View>
                                <Text className="font-bold text-gray-900">Wheat</Text>
                                <Text className="text-gray-500 text-xs">Healthy</Text>
                            </View>
                        </View>
                        <View className="items-end">
                            <View className="bg-green-100 px-2 py-1 rounded-full">
                                <Text className="text-green-600 text-[8px] font-black uppercase">None</Text>
                            </View>
                            <Text className="text-gray-400 text-[10px] mt-1">1d ago</Text>
                        </View>
                    </View>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
