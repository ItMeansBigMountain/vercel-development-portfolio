package genspark.assignments.section7;

import genspark.assignments.Assignment;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public class QueryTheFile implements Assignment {
    public ArrayList<String> solution() {

        //OPEN FILE
        //STORE ALL LINES INTO AN ARRAY-LIST BUT FILTER( ANY LINE THAT CONTAINS A TWO )


        try
        {
            Path p = Paths.get(System.getProperty("user.dir") + "/src/main/resources/filter_problem.text");
            ArrayList<String> output = (ArrayList<String>) Arrays.stream(Files.readString(p, StandardCharsets.UTF_8)
                            .split("\n"))
                    .filter(line -> !line.contains("2"))
                    .collect(Collectors.toList());

            System.out.println(output);
            return output;
        }


        catch (Exception ignored){}
        return null;







    }
}
