import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';

export default function ProfileScreen() {
    const navigation = useNavigation();

    return (
        <SafeAreaView className="flex-1 bg-white p-6">
            <Text className="text-2xl font-bold mb-6">Profile</Text>

            <View className="mb-8 items-center">
                <View className="w-24 h-24 bg-green-100 rounded-full items-center justify-center mb-3">
                    <Text className="text-3xl font-bold text-green-700">FJ</Text>
                </View>
                <Text className="text-xl font-bold">Farmer John</Text>
                <Text className="text-gray-500">farmer@example.com</Text>
            </View>

            <View className="space-y-4">
                <TouchableOpacity
                    className="p-4 bg-gray-50 rounded-xl"
                    onPress={() => navigation.navigate('Login')} // Mock logout
                >
                    <Text className="text-red-600 font-medium text-center">Log Out</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}
