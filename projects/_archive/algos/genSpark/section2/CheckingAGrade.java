import java.text.MessageFormat;

public class CheckingAGrade {
    public static String solution(int grade) {
        if (grade < 70)
            return "F";
        else if (grade >= 90 && grade <= 100)
            return "A";
        else if (grade >= 80 && grade <= 89)
            return "B";
        else
            return "C";
    }

    public static void main(String[] args) {
        for (int x = 10; x <= 100; x = x + 10) {
            System.out.println(MessageFormat.format("{0} : {1}", x, solution(x)));
        }
    }
}
