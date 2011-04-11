
import java.io.*;
import weka.core.Instances
import weka.classifiers.trees.J48
import weka.classifiers.functions.MultilayerPerceptron

public class Test{
	public static void main(String[] args){

		try{
			Runtime r = Runtime.getRuntime();
			final Process p = r.exec("python main.py");

			// Consommation de la sortie standard de l'application externe dans un Thread separe
			new Thread() {
				public void run() {
					try {
						BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
						String line = "";
						try {
							while((line = reader.readLine()) != null) {
								System.out.println("Sortie standard");
								System.out.println(line);
								// Traitement du flux de sortie de l'application si besoin est
							}
						} finally {
							reader.close();
						}
					} catch(IOException ioe) {
						ioe.printStackTrace();
					}
				}
			}.start();

			// Consommation de la sortie d'erreur de l'application externe dans un Thread separe
			new Thread() {
				public void run() {
					try {
						BufferedReader reader = new BufferedReader(new InputStreamReader(p.getErrorStream()));
						String line = "";
						try {
							while((line = reader.readLine()) != null) {
								System.out.println("Erreurs");
								System.out.println(line);
								// Traitement du flux d'erreur de l'application si besoin est
							}
						} finally {
							reader.close();
						}
					} catch(IOException ioe) {
						ioe.printStackTrace();
					}
				}
			}.start();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
}
