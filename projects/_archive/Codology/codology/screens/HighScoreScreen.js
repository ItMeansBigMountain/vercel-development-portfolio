import React, { useEffect, useState } from 'react';
import {
    ActivityIndicator,
    Pressable,
    ScrollView,
    StyleSheet,
    Text,
    View,
} from 'react-native';

const API_URL = 'https://codology-api.vercel.app/api';

const HighScoreScreen = () => {
    const [highscores, setHighscores] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [message, setMessage] = useState('');

    const fetchHS = async () => {
        setIsLoading(true);
        setMessage('');
        try {
            const response = await fetch(`${API_URL}/highscores`);
            const jsonRes = await response.json();
            if (!response.ok) {
                setMessage(jsonRes.message || 'Could not load leaderboard.');
                setHighscores([]);
                return;
            }
            setHighscores(Array.isArray(jsonRes.highscores) ? jsonRes.highscores : []);
        } catch (err) {
            console.log(err);
            setMessage('Could not load leaderboard.');
            setHighscores([]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchHS();
    }, []);

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <View style={styles.card}>
                <Text style={styles.title}>Leaderboard</Text>
                <Text style={styles.helperText}>Top Codology runs ranked by score, then fastest time.</Text>

                {isLoading ? <ActivityIndicator color="darkslateblue" /> : null}
                {message ? <Text style={styles.message}>{message}</Text> : null}

                {!isLoading && !message && highscores.length === 0 ? (
                    <Text style={styles.emptyText}>No scores yet. Play a round and be first.</Text>
                ) : null}

                {highscores.map((row, index) => (
                    <View key={`${row.username}-${row.timestamp || index}`} style={styles.row}>
                        <Text style={styles.rank}>#{index + 1}</Text>
                        <View style={styles.nameColumn}>
                            <Text style={styles.name}>{row.username || 'Player'}</Text>
                            <Text style={styles.time}>{Number(row.time || 0)} seconds</Text>
                        </View>
                        <Text style={styles.score}>{Number(row.score || 0)} pts</Text>
                    </View>
                ))}

                <Pressable style={styles.refreshButton} onPress={fetchHS}>
                    <Text style={styles.refreshButtonText}>Refresh</Text>
                </Pressable>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#f4f1ff',
    },
    card: {
        width: '100%',
        maxWidth: 720,
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 24,
    },
    title: {
        color: 'darkslateblue',
        fontSize: 34,
        fontWeight: '800',
        textAlign: 'center',
        marginBottom: 8,
    },
    helperText: {
        color: '#3d375c',
        fontSize: 16,
        textAlign: 'center',
        marginBottom: 20,
    },
    row: {
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomColor: '#ece8ff',
        borderBottomWidth: 1,
        paddingVertical: 14,
        gap: 12,
    },
    rank: {
        width: 48,
        color: 'darkslateblue',
        fontSize: 18,
        fontWeight: '800',
    },
    nameColumn: {
        flex: 1,
    },
    name: {
        fontSize: 18,
        fontWeight: '700',
        color: '#241a4a',
    },
    time: {
        color: '#6e6790',
        marginTop: 2,
    },
    score: {
        fontSize: 18,
        fontWeight: '800',
        color: '#18884f',
    },
    message: {
        color: '#b64242',
        fontWeight: '700',
        textAlign: 'center',
        marginVertical: 14,
    },
    emptyText: {
        color: '#6e6790',
        textAlign: 'center',
        marginVertical: 18,
        fontSize: 16,
    },
    refreshButton: {
        backgroundColor: 'darkslateblue',
        borderRadius: 25,
        paddingVertical: 13,
        alignItems: 'center',
        marginTop: 20,
    },
    refreshButtonText: {
        color: '#ffffff',
        fontSize: 16,
        fontWeight: '700',
    },
});

export default HighScoreScreen;
