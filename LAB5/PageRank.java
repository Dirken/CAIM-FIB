import java.util.HashMap;
import java.util.ArrayList;
import java.io.*;
import java.util.Arrays;

public class PageRank {

  static class Edge {
      int origin;     // modified, instead of destination we use origin
      int weight;   // number of routes in this edge
  }

  static class EdgeList {
      int weight;    // total number of edges = sum of second components of list
      ArrayList<Edge> list;
      HashMap<Integer, Edge> listAux; //additional structure added to the original code
  }

  static class ResultRank {
    int incoming;
    int outgoing;
    double rankPosition;
    String airportCode;   //static String airportCodes[]; index to short code
    
    String airportName;  //static String airportNames[]; index to airport name
  }

  static HashMap<String,Integer> airportIndices;  // airport code to index
  static EdgeList[] G;    
  static ResultRank[] result; //Array where we're going to store our result
  static double[] airportRank; //Ranking of each airport

  public static void readAirports() {
    try {
      //We read the data from airports.txt
      String fileName = "airports.txt";
      System.out.println("... opening file "+fileName);
      FileInputStream fstream = new FileInputStream(fileName);
      DataInputStream in = new DataInputStream(fstream);
      BufferedReader br = new BufferedReader(new InputStreamReader(in));

      //initialize data structures:
      String strLine;
      int index = 0;
      ArrayList<String> codeTemp = new ArrayList<String>();
      ArrayList<String> nameTemp = new ArrayList<String>();
      airportIndices = new HashMap<String, Integer>();


      //read airports content 
      while ((strLine = br.readLine()) != null) {
          String[] aLine = strLine.split(",");
          String airportCode = aLine[4];
          String airportName = aLine[1].substring(1, aLine[1].length() - 1) + " (" + aLine[3].substring(1, aLine[3].length() - 1) + ")";
          if (airportCode.length() > 2) {
              airportCode = airportCode.substring(1, airportCode.length() - 1);
              codeTemp.add(airportCode);
              nameTemp.add(airportName);
              airportIndices.put(airportCode, index); 
              index++;
          }
      }
      //initialize data structures that need index as value:
      G = new EdgeList[index];
      result = new ResultRank[index];
      airportRank = new double[index];
      final double initialValueRank = 1.0/index;

      
      for (int i = 0; i < index; i++) {
           result[i] = new ResultRank();
           result[i].outgoing = result[i].incoming = 0;
           result[i].airportCode = codeTemp.get(i);
           result[i].airportName = nameTemp.get(i);

           G[i] = new EdgeList();
           G[i].weight = 0;
           G[i].list = new ArrayList<Edge>();
           G[i].listAux = new HashMap<Integer, Edge>();
           airportRank[i] = result[i].rankPosition = initialValueRank;
      }
      System.out.println("... "+index+" airports read");

      in.close();
       
      }catch (Exception e){
	     //Catch exception if any
           System.err.println("Error: " + e.getMessage());
           // return null;
      }
  }


     public static void readRoutes() {
      try {
        String fileName = "routes.txt";
        System.out.println("... opening file "+fileName);
        FileInputStream fstream = new FileInputStream(fileName);
        DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));

        String strLine;
        int index = 0;
        while ((strLine = br.readLine()) != null) {
            String[] aLine = strLine.split(",");
            Integer comesFrom = airportIndices.get(aLine[2]);
            Integer goesTo = airportIndices.get(aLine[4]);
            if (comesFrom != null && goesTo != null){
              G[comesFrom].weight++;
              Edge tempComesFrom = G[goesTo].listAux.get(comesFrom);
              result[comesFrom].outgoing++;
              result[goesTo].incoming++;
              if (tempComesFrom == null) {
                  tempComesFrom = new Edge();
                  tempComesFrom.origin = comesFrom;
                  tempComesFrom.weight = 1;
                  G[goesTo].listAux.put(comesFrom, tempComesFrom);
                  G[goesTo].list.add(tempComesFrom);
              } else {
                  tempComesFrom.weight++;
              }
            }        
            ++index;
        }

        System.out.println("... "+index+" routes read");

        in.close();

      } catch (Exception e){
        //Catch exception if any
        System.err.println("Error: " + e.getMessage());
        // return null;
      }
    }

  public static int computePageRanks() {
    int steps = 0;                                  
    int maxsteps = 1000000;
    double[] tmpRank = new double[airportRank.length];
    double auxPR = 0.0;   
    double damp = 0.85;    
    double precision = 0.001;                    
    
    for (int i = 0; i < airportRank.length; ++i) if (G[i].weight == 0) auxPR += airportRank[i]/(double)airportRank.length;

    while (steps < maxsteps) {
        int counter = 0;                         
        double plusPR = 0.0;                   
        double totalRank = 0.0;
        for (int i = 0; i < airportRank.length; ++i) {
            tmpRank[i] = 0.0;
            for (int j = 0; j < G[i].list.size(); ++j) {
                tmpRank[i] += airportRank[G[i].list.get(j).origin] * ((double)(G[i].list.get(j).weight)) / ((double)(G[G[i].list.get(j).origin].weight));
            }
            tmpRank[i] += auxPR;
            tmpRank[i] = (1.0 - damp)/(double)airportRank.length + damp*tmpRank[i];
            counter += (Math.abs(airportRank[i] - tmpRank[i]) > precision) ? 1 : 0;
            if (G[i].weight == 0) plusPR += tmpRank[i]/(double)airportRank.length;
        }
        auxPR = plusPR;
        double[] auxSwap = airportRank;
        airportRank = tmpRank;
        tmpRank = auxSwap;
        if (counter == 0) break;
        ++steps;
    }
    for (int i = 0; i < airportRank.length; ++i) result[i].rankPosition = airportRank[i];


    int num =0;
    return steps;
  }

  public static void outputPageRanks() {

    java.util.Arrays.sort(result, new java.util.Comparator<ResultRank>() {
                      public int compare(ResultRank r1, ResultRank r2) {
                          if (r1.rankPosition < r2.rankPosition) return -1;
                          else if (r1.rankPosition > r2.rankPosition) return 1;
                          else return 0;
                      }
                  });
    double suma = 0;
    for (int i = 0; i < result.length; ++i) {
        System.out.println(result[i].rankPosition + "\t" + result[i].airportCode);
        suma += result[i].rankPosition;
    }
    System.out.println(suma);

  }

  public static void main(String args[])  {

     readAirports();   // get airport names, codes, and assign indices
     readRoutes();     // read tuples and build graph
     computePageRanks();
     outputPageRanks(); 

  }
    
}
