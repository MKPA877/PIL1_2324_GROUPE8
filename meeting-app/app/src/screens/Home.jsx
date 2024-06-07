import { SafeAreaView, Text } from "react-native"
import { useLayoutEffect} from "react"
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome'

import RequestsScreen from "./Requests"
import FriendsScreen from "./Friends";
import ProfileScreen from "./Profile";




const Tab= createBottomTabNavigator()
 


function HomeScreen ({navigation}) {
   
    useLayoutEffect(() => {
        navigation.setOptions({
            headerShown: false
        })
    }, [])


    return (
        <Tab.Navigator
        screenOptions={({ route, navigation })=> ({
            headerRight:() => {
                <TouchableOpacity>
                  <FontAwesomeIcon 
                  style={{marginRight:16}}
                  icon='magnifying-glass' s
                  ize={22} 
                  color='#404040'
                  />      
                </TouchableOpacity>
            },
            tabBarIcon:({ focused, color, size})=> {
             cont icons= {
                Requests: 'bell',
                Friends:'inbox'
                Profile:'user'
             }
             const icon = icons[route.name]
             return(
                <FontAwesomeIcon icon={icon} size={28} color={color}/>
             )
            },
            tabBarActiveTinColor:'#202020',
            tabBarShowLabel: false

        })}
        >
            <Tab.Screen name="Requests"  component={RequestsScreen}/>
            <Tab.Screen name="Friends"   component={FriendsScreen}/>
            <Tab.Screen name="Profile"   component={ProfileScreen}/>
        </Tab.Navigator>  
    )
}


export default HomeScreen