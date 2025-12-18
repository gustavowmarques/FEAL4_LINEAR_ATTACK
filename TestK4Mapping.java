// TestK4Mapping.java
import java.util.*;

public class TestK4Mapping {
    public static void main(String[] args) throws Exception {
        // create a key with distinct bytes for K4 and K5
        int[] key = new int[6];
        key[0] = key[1] = key[2] = key[3] = 0;
        key[4] = 0x01020304; // K4 (distinct bytes 01 02 03 04)
        key[5] = 0x0a0b0c0d; // K5 (distinct bytes 0a 0b 0c 0d)

        byte[] pt = new byte[8];
        for (int i = 0; i < 8; i++) pt[i] = (byte) (0x10 + i); // 10 11 12 13 14 15 16 17

        // make a copy for printing original plaintext after encrypt modifies it
        byte[] ptCopy = Arrays.copyOf(pt, pt.length);

        // call FEAL encrypt (in-place)
        FEAL.encrypt(pt, key);

        // print results
        System.out.printf("Plaintext:      %s%n", bytesHex(ptCopy));
        System.out.printf("Ciphertext:     %s%n", bytesHex(pt));
        System.out.printf("K4 word hex:    0x%08x  bytes (MSB->LSB): %02x %02x %02x %02x%n",
            key[4],
            (key[4] >> 24) & 0xff, (key[4] >> 16) & 0xff, (key[4] >> 8) & 0xff, key[4] & 0xff);
        System.out.printf("K5 word hex:    0x%08x  bytes (MSB->LSB): %02x %02x %02x %02x%n",
            key[5],
            (key[5] >> 24) & 0xff, (key[5] >> 16) & 0xff, (key[5] >> 8) & 0xff, key[5] & 0xff);

        // compute round intermediates using the usual FEAL final transform:
        // left_final = right_round ^ K4
        // right_final = left_round ^ right_round ^ K5
        // We invert to get right_round and left_round:
        int cL = pack32(pt, 0);
        int cR = pack32(pt, 4);
        int right_round = cL ^ key[4];
        int left_round  = cR ^ right_round ^ key[5];

        System.out.printf("right_round (word)  0x%08x  bytes: %02x %02x %02x %02x%n",
            right_round,
            (right_round >> 24) & 0xff, (right_round >> 16) & 0xff, (right_round >> 8) & 0xff, right_round & 0xff);
        System.out.printf("left_round  (word)  0x%08x  bytes: %02x %02x %02x %02x%n",
            left_round,
            (left_round >> 24) & 0xff, (left_round >> 16) & 0xff, (left_round >> 8) & 0xff, left_round & 0xff);

        // map of output bytes:
        // ciphertext bytes [0..3] are the bytes of left_final (which equals right_round ^ K4)
        // ciphertext bytes [4..7] are the bytes of right_final (which equals left_round ^ right_round ^ K5)
    }

    static int pack32(byte[] b, int off) {
        return ((b[off] & 0xff) << 24) | ((b[off+1] & 0xff) << 16) | ((b[off+2] & 0xff) << 8) | (b[off+3] & 0xff);
    }

    static String bytesHex(byte[] a) {
        StringBuilder sb = new StringBuilder();
        for (byte bb : a) sb.append(String.format("%02x ", bb & 0xff));
        return sb.toString().trim();
    }
}
