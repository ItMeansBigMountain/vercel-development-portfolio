import java.util.Arrays;

public class FrequencyCounter {
    // FREQUENCY FINDER
    // DISPLAYS FREQUENCIES IN ARRAY
    public static int[] frequencies_of_values(int[] arr) {
        // find frequencies of all arrs
        int[] fr = new int[arr.length];
        int visited = -1;

        for (int i = 0; i < arr.length; i++) {
            int count = 1;
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] == arr[j]) {
                    count++;
                    // To avoid counting same element again
                    fr[j] = visited;
                }
            }
            if (fr[i] != visited)
                fr[i] = count;
        }

        // Displays the frequency of each element present in array
        for (int i = 0; i < fr.length; i++) {
            if (fr[i] != visited)
                System.out.println("    " + arr[i] + "    |    " + fr[i]);
        }

        return fr;
    }

    public static void main(String[] args) {
        System.out
                .println(Arrays.toString(frequencies_of_values(new int[] { 5, 5, 2, 3, 44, 1, 4, 44, 44, 99, 1, 2 })));
    }
}
