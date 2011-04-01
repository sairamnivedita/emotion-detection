
import java.io.*;

public class Python{
	public static void main(String[] args){
		try{
			Runtime r = Runtime.getRuntime();
			Process p = r.exec("python face_detect.py");
			p.waitFor();
			BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
			String line = "";
			while((line = br.readLine()) != null){
				System.out.println("SALUT ca marche????");
				System.out.println("line = "+line);
			}
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
}
