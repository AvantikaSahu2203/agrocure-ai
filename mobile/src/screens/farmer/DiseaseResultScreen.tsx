import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, Image, Linking, Share } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRoute, useNavigation } from '@react-navigation/native';
import { 
    AlertTriangle, 
    ShoppingBag, 
    ArrowLeft, 
    Share2, 
    CheckCircle2, 
    Info, 
    ExternalLink,
    MapPin,
    Thermometer,
    Droplets
} from 'lucide-react-native';
import { COLORS, SHADOWS } from '../../theme/theme';

export default function DiseaseResultScreen() {
    const navigation = useNavigation();
    const route = useRoute();
    const { report, ecommerce, imageUrl } = route.params as any || {};

    if (!report) {
        return (
            <SafeAreaView className="flex-1 bg-white items-center justify-center p-6">
                <AlertTriangle color={COLORS.danger} size={48} />
                <Text className="text-xl font-bold mt-4">No data found</Text>
                <TouchableOpacity 
                    className="mt-6 bg-green-600 px-8 py-3 rounded-xl"
                    onPress={() => navigation.goBack()}
                >
                    <Text className="text-white font-bold">Go Back</Text>
                </TouchableOpacity>
            </SafeAreaView>
        );
    }

    const onShare = async () => {
        try {
            await Share.share({
                message: `AgroCure AI Analysis: ${report["🌱 Crop"]} - ${report["🦠 Disease"]}. Treatment: ${report["💊 Treatment"]?.Chemical?.[0] || 'Check app for details'}`,
            });
        } catch (error) {
            console.error(error);
        }
    };

    const openStore = (url: string) => {
        if (url) Linking.openURL(url);
    };

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header */}
            <View className="bg-white p-4 border-b border-gray-100 flex-row items-center justify-between">
                <View className="flex-row items-center">
                    <TouchableOpacity onPress={() => navigation.goBack()} className="mr-4">
                        <ArrowLeft color="black" size={24} />
                    </TouchableOpacity>
                    <Text className="text-lg font-bold">Analysis Report</Text>
                </View>
                <TouchableOpacity onPress={onShare}>
                    <Share2 color="black" size={24} />
                </TouchableOpacity>
            </View>

            <ScrollView className="flex-1">
                {/* Image & Main Info */}
                <View className="p-6 bg-white mb-2" style={SHADOWS.sm}>
                    <View className="rounded-3xl overflow-hidden mb-6">
                        <Image source={{ uri: imageUrl }} className="w-full h-64" resizeMode="cover" />
                        <View className="absolute top-4 right-4 bg-red-600 px-4 py-1 rounded-full">
                            <Text className="text-white font-bold">{report["📊 Confidence"]}</Text>
                        </View>
                    </View>

                    <View className="items-center mb-4">
                        <Text className="text-gray-500 text-sm">{report["🌱 Crop"]}</Text>
                        <Text className="text-2xl font-black text-gray-900 text-center">{report["🦠 Disease"]}</Text>
                    </View>

                    <View className="flex-row justify-center gap-4">
                        <View className="flex-row items-center bg-orange-50 px-3 py-1 rounded-full border border-orange-100">
                            <AlertTriangle color="#f97316" size={14} />
                            <Text className="text-orange-700 text-xs font-bold ml-1">High Risk</Text>
                        </View>
                        <View className="flex-row items-center bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
                            <MapPin color="#2563eb" size={14} />
                            <Text className="text-blue-700 text-xs font-bold ml-1">{report["🌍 Location Context"]}</Text>
                        </View>
                    </View>
                </View>

                {/* Symptoms */}
                <View className="p-6 bg-white mb-2" style={SHADOWS.sm}>
                    <View className="flex-row items-center gap-2 mb-4">
                        <Info color={COLORS.primary} size={20} />
                        <Text className="text-lg font-bold">Detected Symptoms</Text>
                    </View>
                    <View className="flex-row flex-wrap gap-2">
                        {report["🔍 Symptoms"]?.map((s: string, i: number) => (
                            <View key={i} className="bg-gray-100 px-4 py-2 rounded-xl">
                                <Text className="text-gray-700">{s}</Text>
                            </View>
                        ))}
                    </View>
                </View>

                {/* Treatment Section */}
                <View className="p-6 bg-white mb-2" style={SHADOWS.sm}>
                    <View className="flex-row items-center gap-2 mb-4">
                        <CheckCircle2 color={COLORS.primary} size={20} />
                        <Text className="text-lg font-bold">AgriAI Recommendation</Text>
                    </View>

                    <View className="space-y-4">
                        {report["💊 Treatment"]?.Chemical?.length > 0 && (
                            <View>
                                <Text className="font-bold text-gray-900 mb-2">Chemical Treatment</Text>
                                {report["💊 Treatment"].Chemical.map((t: string, i: number) => (
                                    <View key={i} className="bg-green-50 p-4 rounded-xl border border-green-100 mb-2">
                                        <Text className="text-green-800 font-medium">{t}</Text>
                                    </View>
                                ))}
                            </View>
                        )}
                        
                        <View className="bg-blue-50 p-4 rounded-xl border border-blue-100 mt-2">
                            <Text className="text-blue-500 font-bold text-xs uppercase mb-1">Dosage Advice</Text>
                            <Text className="text-blue-700 leading-5">{report["🧪 Dosage"]}</Text>
                        </View>
                    </View>
                </View>

                {/* Weather Advice */}
                <View className="p-6 bg-white mb-2" style={SHADOWS.sm}>
                     <View className="flex-row items-center gap-2 mb-4">
                        <Thermometer color={COLORS.warning} size={20} />
                        <Text className="text-lg font-bold">Weather-Safe Spraying</Text>
                    </View>
                    <View className="bg-orange-50 p-4 rounded-2xl border border-orange-100">
                        <Text className="text-gray-900 leading-6 italic">"{report["🌡️ Weather Advice"]}"</Text>
                    </View>
                </View>

                {/* Market Links */}
                <View className="p-6 bg-white mb-10" style={SHADOWS.sm}>
                    <Text className="text-lg font-bold mb-4">Buy Medicine Online</Text>
                    <View className="flex-row gap-4">
                        {ecommerce?.amazon && (
                            <TouchableOpacity 
                                className="flex-1 bg-[#232f3e] p-4 rounded-2xl items-center"
                                onPress={() => openStore(ecommerce.amazon)}
                            >
                                <Text className="text-white font-bold">Amazon</Text>
                                <ExternalLink color="white" size={14} />
                            </TouchableOpacity>
                        )}
                        {ecommerce?.flipkart && (
                            <TouchableOpacity 
                                className="flex-1 bg-[#2874f0] p-4 rounded-2xl items-center"
                                onPress={() => openStore(ecommerce.flipkart)}
                            >
                                <Text className="text-white font-bold">Flipkart</Text>
                                <ExternalLink color="white" size={14} />
                            </TouchableOpacity>
                        )}
                    </View>
                    {ecommerce?.maps && (
                        <TouchableOpacity 
                            className="mt-4 bg-gray-100 p-4 rounded-2xl flex-row items-center justify-center gap-2"
                            onPress={() => openStore(ecommerce.maps)}
                        >
                            <MapPin color="black" size={18} />
                            <Text className="font-bold">Find on Google Maps</Text>
                        </TouchableOpacity>
                    )}
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
