// Verifier.java
import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Verifier {
    static class Pair { byte[] pt; byte[] ct; Pair(byte[] p, byte[] c){pt=p;ct=c;} }

    static List<Pair> loadPairs(String fname) throws Exception {
        List<Pair> list = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(fname));
        String line;
        String pendingPlain = null;
        Pattern hexp = Pattern.compile("([0-9a-fA-F]{16})");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.length() == 0) continue;
            // look for a 16-hex substring anywhere
            Matcher m = hexp.matcher(line);
            if (m.find()) {
                String hex = m.group(1);
                if (line.toLowerCase().startsWith("plaintext")) {
                    pendingPlain = hex;
                } else if (line.toLowerCase().startsWith("ciphertext")) {
                    if (pendingPlain == null) throw new RuntimeException("Ciphertext without preceding Plaintext");
                    byte[] pt = hexToBytes(pendingPlain);
                    byte[] ct = hexToBytes(hex);
                    list.add(new Pair(pt, ct));
                    pendingPlain = null;
                } else {
                    // Fallback: if the file had single-line "pt ct" pairs we'd handle it,
                    // but here we only expect the labelled format. Try to be robust:
                    // If pendingPlain is null, treat this hex as plaintext and wait for ciphertext.
                    if (pendingPlain == null) pendingPlain = hex;
                    else {
                        byte[] pt = hexToBytes(pendingPlain);
                        byte[] ct = hexToBytes(hex);
                        list.add(new Pair(pt, ct));
                        pendingPlain = null;
                    }
                }
            }
        }
        br.close();
        if (pendingPlain != null) throw new RuntimeException("File ended with unmatched Plaintext");
        return list;
    }

    static byte[] hexToBytes(String s) {
        s = s.replaceAll("[^0-9a-fA-F]","");
        int len = s.length()/2;
        byte[] b = new byte[len];
        for (int i=0;i<len;i++) b[i] = (byte) Integer.parseInt(s.substring(2*i,2*i+2),16);
        return b;
    }

    static String bytesHex(byte[] a){
        StringBuilder sb = new StringBuilder();
        for (byte bb : a) sb.append(String.format("%02x", bb & 0xff));
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 6) {
            System.out.println("Usage: java Verifier K0 K1 K2 K3 K4 K5   (each K as 8-hex digits, e.g. 63cab942)");
            System.exit(1);
        }
        int[] key = new int[6];
        for (int i=0;i<6;i++) key[i] = (int) Long.parseLong(args[i], 16);

        List<Pair> pairs = loadPairs("known.txt");
        System.out.println("Loaded " + pairs.size() + " pairs. Verifying...");

        for (int i=0;i<pairs.size();i++) {
            byte[] pt = Arrays.copyOf(pairs.get(i).pt, 8);
            // encrypt using FEAL.encrypt (in-place)
            FEAL.encrypt(pt, key);
            String ctCalc = bytesHex(pt);
            String ctGiven = bytesHex(pairs.get(i).ct);
            if (!ctCalc.equals(ctGiven)) {
                System.out.printf("Mismatch at index %d\n", i);
                System.out.printf("Plaintext: %s\n", bytesHex(pairs.get(i).pt));
                System.out.printf("Expected : %s\n", ctGiven);
                System.out.printf("Computed : %s\n", ctCalc);
                System.exit(2);
            }
        }
        System.out.println("All pairs matched. Key set VERIFIED.");
    }
}
