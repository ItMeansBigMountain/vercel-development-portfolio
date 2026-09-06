import React from "react";
import { TouchableOpacity, Text, StyleSheet , View } from "react-native";

const CButton = ({ text, action, bg }) => {

    return (
        <TouchableOpacity style={{backgroundColor:bg }} onPress={action}>
            <View style={styles.button} >
                <Text style={styles.text}>{text}</Text>
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    button: {
        // backgroundColor: CButton.bg,
        padding: 18,
        // width: "46%",
        // height: "10%",
    },
    text: {
        fontSize: 18,
        color: "white",
        textAlign: "center",
    },
});

export default CButton;