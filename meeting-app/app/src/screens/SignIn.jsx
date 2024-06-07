import { SafeAreaView, Text, View } from "react-native";
import Title from "../common/Tile";
import { useLayoutEffect } from "react"
import Input from "../common/Input";
import Button from "../common/Button";













function SignInScreen ({navigation}) {
    
    useLayoutEffect(() => {
        navigation.setOptions({
            headerShown: false
        })
    }, [])

    return (
        <SafeAreaView style={{ flex: 1 }}> 
        <View 
            style={{ 
                flex: 1, 
                justifyContent: 'center', 
                paddingHorizontal: 20
            }}
        > 
         <Title text='RealtimeChat' color='#202020' />

         <Input title='Username'/>
         <Input title='Password'/>

            <Button title='Sign In'/>

            <Text style={{ textAlign:'center', marginTop: 40}}>
                Don't have an account? <Text 
                style={{ color: 'blue'}}
                onPress={() => navigation.navigate('SignUp')}
                >
                    Sign Up
                </Text>
            </Text>

        </View>
        </SafeAreaView>
    )
}


export default SignInScreen