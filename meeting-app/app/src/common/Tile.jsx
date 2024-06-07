import { Text } from "react-native"




function Title({ text, color }) {
    return (
        <Text 
            style={{
                color: color,
                textAlign: 'center',
                fontSize: 48,
                fontFamily: 'RobotoSlab-VariableFont_wght'
            }}
        >
            { text }
        </Text>
    )
}

export default Title