import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';

export default function LoginScreen() {
    const navigation = useNavigation();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = () => {
        // Mock login
        if (email && password) {
            navigation.reset({
                index: 0,
                routes: [{ name: 'FarmerDashboard' }],
            });
        } else {
            Alert.alert("Error", "Please enter email and password");
        }
    };

    return (
        <SafeAreaView className="flex-1 bg-white p-6 justify-center">
            <Text className="text-3xl font-bold text-gray-900 mb-8">Welcome Back</Text>

            <View className="space-y-4">
                <View>
                    <Text className="text-gray-700 font-medium mb-1">Email</Text>
                    <TextInput
                        className="w-full border border-gray-300 rounded-lg p-3 bg-gray-50"
                        placeholder="farmer@example.com"
                        value={email}
                        onChangeText={setEmail}
                        autoCapitalize="none"
                    />
                </View>

                <View>
                    <Text className="text-gray-700 font-medium mb-1">Password</Text>
                    <TextInput
                        className="w-full border border-gray-300 rounded-lg p-3 bg-gray-50 mb-6"
                        placeholder="********"
                        value={password}
                        onChangeText={setPassword}
                        secureTextEntry
                    />
                </View>

                <TouchableOpacity
                    className="w-full bg-green-600 py-4 rounded-xl items-center"
                    onPress={handleLogin}
                >
                    <Text className="text-white font-bold text-lg">Log In</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}
