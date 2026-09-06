import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
    ActivityIndicator,
    Pressable,
    ScrollView,
    StyleSheet,
    Text,
    TextInput,
    View,
} from 'react-native';
import { useNavigation } from '@react-navigation/core';
import axios from 'axios';
import { basic13Questions, totalBasic13Challenges } from '../data/basic13Questions';

const API_URL = 'https://codology-api.vercel.app/api';
const questions = basic13Questions;

const HomeScreen = () => {
    const navigation = useNavigation();
    const timerRef = useRef(null);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [score, setScore] = useState(0);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isGameStarted, setIsGameStarted] = useState(false);
    const [isGameOver, setIsGameOver] = useState(false);
    const [timer, setTimer] = useState(0);
    const [playerName, setPlayerName] = useState('');
    const [submitMessage, setSubmitMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const finalScore = useMemo(() => score, [score]);
    const question = questions[questionIndex];

    useEffect(() => {
        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, []);

    const startGame = () => {
        setQuestionIndex(0);
        setScore(0);
        setSelectedOption(null);
        setTimer(0);
        setPlayerName('');
        setSubmitMessage('');
        setIsGameOver(false);
        setIsGameStarted(true);

        if (timerRef.current) clearInterval(timerRef.current);
        timerRef.current = setInterval(() => {
            setTimer((prevTime) => prevTime + 1);
        }, 1000);
    };

    const finishGame = (nextScore) => {
        if (timerRef.current) clearInterval(timerRef.current);
        setScore(nextScore);
        setIsGameOver(true);
        setIsGameStarted(false);
        setSelectedOption(null);
    };

    const handleAnswerSelection = (selectedAnswerIndex) => {
        if (selectedOption !== null) return;

        const wasCorrect = selectedAnswerIndex === question.correctAnswer;
        const nextScore = wasCorrect ? score + 1 : score;

        setSelectedOption(selectedAnswerIndex);
        setScore(nextScore);

        setTimeout(() => {
            if (questionIndex < questions.length - 1) {
                setQuestionIndex(questionIndex + 1);
                setSelectedOption(null);
            } else {
                finishGame(nextScore);
            }
        }, 700);
    };

    const submitHighScore = async () => {
        const cleanName = playerName.trim();
        if (!cleanName) {
            setSubmitMessage('Type your name to join the leaderboard.');
            return;
        }

        setIsSubmitting(true);
        setSubmitMessage('');
        try {
            await axios.post(`${API_URL}/add-highscore`, {
                username: cleanName,
                score: finalScore,
                time: timer,
            });
            navigation.navigate('HighScores');
        } catch (error) {
            console.log('Error posting high score:', error);
            setSubmitMessage('Could not post your score. Try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (isGameOver) {
        return (
            <View style={styles.container}>
                <View style={styles.card}>
                    <Text style={styles.eyebrow}>Basic 13 Review Complete</Text>
                    <Text style={styles.title}>Game Over</Text>
                    <Text style={styles.resultText}>Score: {finalScore} / {questions.length}</Text>
                    <Text style={styles.resultText}>Time: {timer} seconds</Text>
                    <Text style={styles.helperText}>Enter your name to post this run to the leaderboard.</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Your name"
                        value={playerName}
                        onChangeText={setPlayerName}
                        maxLength={24}
                        autoCapitalize="words"
                    />
                    {submitMessage ? <Text style={styles.message}>{submitMessage}</Text> : null}
                    <Pressable
                        style={[styles.primaryButton, isSubmitting && styles.disabledButton]}
                        onPress={submitHighScore}
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Submit to Leaderboard</Text>}
                    </Pressable>
                    <Pressable style={styles.secondaryButton} onPress={startGame}>
                        <Text style={styles.secondaryButtonText}>Play Again</Text>
                    </Pressable>
                </View>
            </View>
        );
    }

    return (
        <ScrollView contentContainerStyle={styles.scrollContainer}>
            {!isGameStarted ? (
                <View style={styles.card}>
                    <Text style={styles.eyebrow}>Python + JavaScript</Text>
                    <Text style={styles.title}>Codology: Basic 13</Text>
                    <Text style={styles.helperText}>
                        Practice the 13 classic beginner algorithm drills. Each challenge appears in both Python and JavaScript, with friendly hints made for kids learning to code.
                    </Text>
                    <View style={styles.statsPill}>
                        <Text style={styles.statsText}>{totalBasic13Challenges} challenges • {questions.length} quiz cards</Text>
                    </View>
                    <Pressable style={styles.primaryButton} onPress={startGame}>
                        <Text style={styles.buttonText}>Start Basic 13 Review</Text>
                    </Pressable>
                    <Pressable style={styles.secondaryButton} onPress={() => navigation.navigate('HighScores')}>
                        <Text style={styles.secondaryButtonText}>View Leaderboard</Text>
                    </Pressable>
                </View>
            ) : (
                <View style={styles.gameCard}>
                    <View style={styles.topRow}>
                        <Text style={styles.timer}>Time: {timer}s</Text>
                        <Text style={styles.score}>Score: {score}</Text>
                    </View>
                    <Text style={styles.progress}>Question {questionIndex + 1} of {questions.length}</Text>
                    <Text style={styles.challengeNumber}>Basic 13 {question.number}</Text>
                    <Text style={styles.prompt}>{question.title}</Text>
                    <View style={styles.languageBadge}>
                        <Text style={styles.languageBadgeText}>{question.language}</Text>
                    </View>
                    <Text style={styles.task}>{question.task}</Text>

                    <View style={styles.codeCard} accessibilityLabel="Code Picture">
                        <Text style={styles.codeTitle}>Code Picture</Text>
                        <Text style={styles.codeSnippet}>{question.codeSnippet}</Text>
                    </View>

                    <Text style={styles.kidTip}>Kid tip: {question.kidTip}</Text>

                    <View style={styles.optionsContainer}>
                        {question.options.map((option, index) => {
                            const isSelected = selectedOption === index;
                            const showResult = selectedOption !== null;
                            const isCorrect = showResult && index === question.correctAnswer;
                            return (
                                <Pressable
                                    key={option}
                                    style={[
                                        styles.optionButton,
                                        isSelected && !isCorrect && styles.buttonSelected,
                                        isCorrect && styles.buttonCorrect,
                                    ]}
                                    onPress={() => handleAnswerSelection(index)}
                                >
                                    <Text style={styles.buttonText}>{option}</Text>
                                </Pressable>
                            );
                        })}
                    </View>
                </View>
            )}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#f4f1ff',
    },
    scrollContainer: {
        flexGrow: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#f4f1ff',
    },
    card: {
        width: '100%',
        maxWidth: 620,
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOpacity: 0.12,
        shadowRadius: 12,
    },
    gameCard: {
        width: '100%',
        maxWidth: 860,
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
    },
    topRow: {
        width: '100%',
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 8,
    },
    eyebrow: {
        color: '#6b5bd6',
        fontSize: 14,
        fontWeight: '900',
        letterSpacing: 1.2,
        textTransform: 'uppercase',
        marginBottom: 6,
    },
    title: {
        color: 'darkslateblue',
        fontSize: 34,
        fontWeight: '800',
        marginBottom: 12,
        textAlign: 'center',
    },
    helperText: {
        color: '#3d375c',
        fontSize: 17,
        textAlign: 'center',
        lineHeight: 24,
        marginBottom: 18,
    },
    statsPill: {
        backgroundColor: '#ebe7ff',
        borderRadius: 999,
        paddingVertical: 8,
        paddingHorizontal: 14,
        marginBottom: 12,
    },
    statsText: {
        color: 'darkslateblue',
        fontWeight: '800',
    },
    timer: {
        fontSize: 18,
        fontWeight: '700',
    },
    score: {
        fontSize: 18,
        fontWeight: '700',
    },
    progress: {
        color: '#6e6790',
        fontWeight: '800',
        marginBottom: 8,
    },
    challengeNumber: {
        color: '#6b5bd6',
        fontSize: 16,
        fontWeight: '900',
        marginBottom: 4,
    },
    prompt: {
        fontSize: 24,
        fontWeight: '800',
        textAlign: 'center',
        marginBottom: 10,
        color: '#241a4a',
    },
    task: {
        color: '#3d375c',
        fontSize: 18,
        textAlign: 'center',
        lineHeight: 25,
        marginBottom: 14,
    },
    languageBadge: {
        backgroundColor: '#241a4a',
        borderRadius: 999,
        paddingVertical: 7,
        paddingHorizontal: 14,
        marginBottom: 10,
    },
    languageBadgeText: {
        color: '#ffffff',
        fontWeight: '900',
    },
    codeCard: {
        width: '100%',
        backgroundColor: '#17132b',
        borderColor: '#6b5bd6',
        borderWidth: 2,
        borderRadius: 18,
        padding: 18,
        marginBottom: 14,
    },
    codeTitle: {
        color: '#bdb6ff',
        fontSize: 13,
        fontWeight: '900',
        marginBottom: 10,
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    codeSnippet: {
        color: '#f8f7ff',
        fontFamily: 'monospace',
        fontSize: 16,
        lineHeight: 23,
    },
    kidTip: {
        width: '100%',
        backgroundColor: '#fff7d6',
        borderRadius: 14,
        color: '#5a4300',
        fontSize: 16,
        fontWeight: '700',
        lineHeight: 22,
        padding: 12,
        marginBottom: 16,
    },
    optionsContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: 12,
        width: '100%',
    },
    optionButton: {
        minWidth: 220,
        maxWidth: 380,
        flexGrow: 1,
        backgroundColor: '#333',
        borderRadius: 20,
        paddingVertical: 14,
        paddingHorizontal: 18,
        alignItems: 'center',
        justifyContent: 'center',
    },
    buttonSelected: {
        backgroundColor: '#b64242',
    },
    buttonCorrect: {
        backgroundColor: '#18884f',
    },
    primaryButton: {
        width: '100%',
        backgroundColor: 'darkslateblue',
        borderRadius: 25,
        paddingVertical: 15,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 8,
    },
    secondaryButton: {
        width: '100%',
        borderColor: 'darkslateblue',
        borderWidth: 2,
        borderRadius: 25,
        paddingVertical: 13,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 12,
    },
    disabledButton: {
        opacity: 0.6,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '700',
        textAlign: 'center',
    },
    secondaryButtonText: {
        color: 'darkslateblue',
        fontSize: 16,
        fontWeight: '700',
    },
    resultText: {
        fontSize: 20,
        fontWeight: '700',
        marginBottom: 8,
    },
    input: {
        width: '100%',
        borderColor: '#c9c1ed',
        borderWidth: 2,
        borderRadius: 16,
        paddingVertical: 12,
        paddingHorizontal: 14,
        fontSize: 18,
        marginBottom: 8,
    },
    message: {
        color: '#b64242',
        fontWeight: '700',
        marginBottom: 6,
    },
});

export default HomeScreen;
