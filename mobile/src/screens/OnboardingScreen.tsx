import React from 'react';
import { View, Text, TouchableOpacity, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { Sprout } from 'lucide-react-native';

export default function OnboardingScreen() {
    const navigation = useNavigation();

    return (
        <SafeAreaView className="flex-1 bg-white items-center justify-center p-6">
            <View className="items-center mb-10">
                <View className="bg-green-100 p-6 rounded-full mb-6">
                    <Sprout size={64} color="#16a34a" />
                </View>
                <Text className="text-3xl font-bold text-gray-900 mb-2 text-center">AgroCure AI</Text>
                <Text className="text-gray-500 text-center text-lg">
                    Detect Plant Diseases Instantly & Get Expert Cures
                </Text>
            </View>

            <TouchableOpacity
                className="w-full bg-green-600 py-4 rounded-xl items-center"
                onPress={() => navigation.navigate('Login')}
            >
                <Text className="text-white font-bold text-lg">Get Started</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}
