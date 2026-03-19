import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, ActivityIndicator, Alert, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Camera, Image as ImageIcon, X, ChevronRight, MapPin } from 'lucide-react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../types/navigation';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';
import apiClient from '../../api/apiClient';
import { COLORS } from '../../theme/theme';

export default function ScanScreen() {
    const navigation = useNavigation<StackNavigationProp<RootStackParamList>>();
    const [image, setImage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [address, setAddress] = useState<{ city: string; state: string } | null>(null);
    const [cropName, setCropName] = useState('Tomato'); // Default for now, can be an input

    useEffect(() => {
        (async () => {
            const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
            const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
            const { status: locationStatus } = await Location.requestForegroundPermissionsAsync();

            if (locationStatus === 'granted') {
                const loc = await Location.getCurrentPositionAsync({});
                setLocation(loc);
                const reverse = await Location.reverseGeocodeAsync({
                    latitude: loc.coords.latitude,
                    longitude: loc.coords.longitude,
                });
                if (reverse.length > 0) {
                    setAddress({
                        city: reverse[0].city || reverse[0].district || 'Unknown',
                        state: reverse[0].region || 'Unknown',
                    });
                }
            }
        })();
    }, []);

    const pickImage = async (useCamera: boolean) => {
        const result = useCamera 
            ? await ImagePicker.launchCameraAsync({ allowsEditing: true, aspect: [4, 4], quality: 0.8 })
            : await ImagePicker.launchImageLibraryAsync({ allowsEditing: true, aspect: [4, 4], quality: 0.8 });

        if (!result.canceled) {
            setImage(result.assets[0].uri);
        }
    };

    const handleAnalyze = async () => {
        if (!image) {
            Alert.alert('Error', 'Please select an image first.');
            return;
        }

        setLoading(true);
        try {
            const formData = new FormData();
            // @ts-ignore
            formData.append('image', {
                uri: image,
                name: 'upload.jpg',
                type: 'image/jpeg',
            });
            formData.append('crop_name', cropName);
            formData.append('city', address?.city || 'Pune');
            formData.append('state', address?.state || 'Maharashtra');
            formData.append('lat', location?.coords.latitude.toString() || '18.5204');
            formData.append('lon', location?.coords.longitude.toString() || '73.8567');
            // Adding some defaults/context
            formData.append('temperature', '28');
            formData.append('humidity', '65');
            formData.append('language', 'en');

            const response = await apiClient.post('/api/v1/orchestrator/full-analysis', formData);
            
            if (response.data.status === 'success') {
                navigation.navigate('DiseaseResult', {
                    report: response.data.agri_ai_report,
                    ecommerce: response.data.ecommerce_links,
                    imageUrl: image
                });
            } else {
                throw new Error('Analysis failed');
            }
        } catch (error) {
            console.error(error);
            Alert.alert('Error', 'Failed to analyze crop image. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <SafeAreaView className="flex-1 bg-white">
            <View className="p-6 border-b border-gray-100 flex-row justify-between items-center">
                <Text className="text-xl font-bold text-gray-900">Scan Crop</Text>
                {image && (
                    <TouchableOpacity onPress={() => setImage(null)}>
                        <X color="gray" size={24} />
                    </TouchableOpacity>
                )}
            </View>

            <ScrollView contentContainerStyle={{ padding: 24 }}>
                {!image ? (
                    <View className="space-y-6">
                        <View className="bg-green-50 p-6 rounded-3xl border border-green-100 items-center">
                            <View className="bg-green-600 p-4 rounded-full mb-4">
                                <Camera color="white" size={32} />
                            </View>
                            <Text className="text-lg font-bold text-gray-900 text-center">Take a Photo</Text>
                            <Text className="text-gray-500 text-center mt-2 leading-5">
                                Ensure the leaf is well-lit and centered in the frame for accurate detection.
                            </Text>
                            <TouchableOpacity 
                                className="bg-green-600 w-full p-4 rounded-2xl mt-6 items-center"
                                onPress={() => pickImage(true)}
                            >
                                <Text className="text-white font-bold text-lg">Open Camera</Text>
                            </TouchableOpacity>
                        </View>

                        <TouchableOpacity 
                            className="flex-row items-center justify-between p-5 bg-gray-50 rounded-2xl border border-gray-100"
                            onPress={() => pickImage(false)}
                        >
                            <View className="flex-row items-center gap-4">
                                <View className="bg-blue-100 p-2 rounded-xl">
                                    <ImageIcon color="#2563eb" size={20} />
                                </View>
                                <Text className="font-bold text-gray-800">Upload from Gallery</Text>
                            </View>
                            <ChevronRight color="gray" size={20} />
                        </TouchableOpacity>

                        <View className="flex-row items-center gap-2 p-4 bg-orange-50 rounded-xl border border-orange-100">
                            <MapPin color="#f97316" size={16} />
                            <Text className="text-orange-700 text-xs font-bold">
                                Location: {address ? `${address.city}, ${address.state}` : 'Fetching...'}
                            </Text>
                        </View>
                    </View>
                ) : (
                    <View className="space-y-6">
                        <View className="rounded-3xl overflow-hidden shadow-lg border-4 border-white">
                            <Image source={{ uri: image }} className="w-full aspect-square" />
                        </View>

                        <View className="bg-gray-50 p-4 rounded-2xl border border-gray-100">
                            <Text className="text-gray-500 text-xs font-bold uppercase tracking-wider mb-1">Selected Crop</Text>
                            <Text className="text-gray-900 font-bold text-lg">Tomato</Text>
                        </View>

                        <TouchableOpacity 
                            className={`p-4 rounded-2xl flex-row items-center justify-center gap-3 ${loading ? 'bg-gray-400' : 'bg-green-600'}`}
                            onPress={handleAnalyze}
                            disabled={loading}
                        >
                            {loading ? (
                                <ActivityIndicator color="white" />
                            ) : (
                                <>
                                    <Text className="text-white font-bold text-lg">Analyze Disease</Text>
                                    <ChevronRight color="white" size={20} />
                                </>
                            )}
                        </TouchableOpacity>

                        <TouchableOpacity 
                            className="p-4 items-center"
                            onPress={() => setImage(null)}
                            disabled={loading}
                        >
                            <Text className="text-gray-500 font-bold">Retake Photo</Text>
                        </TouchableOpacity>
                    </View>
                )}
            </ScrollView>
        </SafeAreaView>
    );
}
