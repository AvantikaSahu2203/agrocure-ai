import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text } from 'react-native';
import { Sprout, Camera, User, Home } from 'lucide-react-native';

// Screen Imports (Placeholders until implemented)
import OnboardingScreen from '../screens/OnboardingScreen';
import LoginScreen from '../screens/auth/LoginScreen';
import DashboardScreen from '../screens/farmer/DashboardScreen';
import ScanScreen from '../screens/farmer/ScanScreen';
import ProfileScreen from '../screens/farmer/ProfileScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function FarmerTabs() {
    return (
        <Tab.Navigator
            screenOptions={{
                headerShown: false,
                tabBarActiveTintColor: '#16a34a',
                tabBarInactiveTintColor: 'gray',
            }}
        >
            <Tab.Screen
                name="Home"
                component={DashboardScreen}
                options={{
                    tabBarIcon: ({ color, size }) => <Home color={color} size={size} />,
                }}
            />
            <Tab.Screen
                name="Scan"
                component={ScanScreen}
                options={{
                    tabBarIcon: ({ color, size }) => <Camera color={color} size={size} />,
                    tabBarStyle: { display: 'none' } // Hide tab bar on camera screen
                }}
            />
            <Tab.Screen
                name="Profile"
                component={ProfileScreen}
                options={{
                    tabBarIcon: ({ color, size }) => <User color={color} size={size} />,
                }}
            />
        </Tab.Navigator>
    );
}

export default function AppNavigator() {
    return (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
            <Stack.Screen name="Onboarding" component={OnboardingScreen} />
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="FarmerDashboard" component={FarmerTabs} />
            <Stack.Screen name="DiseaseResult" getComponent={() => require('../screens/farmer/DiseaseResultScreen').default} />
        </Stack.Navigator>
    );
}
