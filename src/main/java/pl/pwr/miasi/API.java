package pl.pwr.miasi;

public class API {
    public static String parse(String program) {
        return new VisitorInitializer().initialize(program);
    }
}
