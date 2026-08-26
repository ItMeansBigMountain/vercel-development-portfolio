package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.HashMap;

public class CreateAHuman implements Assignment {
    public HashMap<String, Object> solution(String name, Long age) {

        //USING OBJECT AS VALUE SO THAT ANYTHING GOES
        HashMap<String,Object> human = new HashMap<String,Object>();
        human.put("name", name);
        human.put("age", age);
        return human;
    }
}
