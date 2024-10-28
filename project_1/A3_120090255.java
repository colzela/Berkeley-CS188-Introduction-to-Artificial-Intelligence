import java.util.Scanner;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Comparator;
import java.util.Stack;

class State{
    private final byte board[];
    private final int cost;         //g(n)
    private final int weight;       //f(n)
    
    public State(byte b[], int _cost){
        this.board = b;
        cost = _cost;
        weight = cost + hurestic();
    }

    public byte[] getBoard(){
        return this.board;
    }

    public int getCost(){
        return this.cost;
    }

    public int getWeight(){
        return this.weight;
    }

    private int hurestic(){         //h(n), manhaten distance
        int h = 0;
        for(int i = 0; i < board.length; i++){
            if(board[i] == 0) continue;
            int dr = Math.abs(i/3 - (board[i]-1)/3);
            int dc = Math.abs(i%3 - (board[i]-1)%3);
            h += dr + dc;
        }
        return h;
    }

    public ArrayList<State> getNextStates(){
        ArrayList<State> states = new ArrayList<>();
                
        //try every move, if a move changes the board, then it's a valid move (will not go back)
        for(BoardControl.MOVES move : BoardControl.MOVES.values()){
            byte newBoard[] = this.board.clone();
            BoardControl.move(newBoard, move);
            if(!Arrays.equals(this.board, newBoard)){
                states.add(new State(newBoard, this.cost + 1));
            }
        }
        return states;
    }

    public int compareTo(State o) {
        return this.weight - o.weight;
    } 
}

class Solvers{
    public static enum SOLVE_METHOD{A_STAR};
    public static byte[] finalBoard = {1, 2, 3, 4, 5, 6, 7, 8, 0}; 
    
    //to count the number of expanded nodes
    public static long times;
    
    //takes a byte array and returns it as a string for the map to hash
    public static String stringify(byte[] arr){
        String str = "";
        for(int i = 0 ; i < arr.length ; ++i){
            str += String.valueOf(arr[i]);
        }
        return str;
    }

    //solve the current position with A* search
    public static Map<String, byte[]> aStar(byte[] current){
        Map<String, Integer> dist = new HashMap<>();              //string : manhattan distance
        Map<String, byte[]> parent = new HashMap<>();             //kid : parent
        
        PriorityQueue<State> q = new PriorityQueue<>(new Comparator<State>() {  
            @Override                                       
            //override the rule to add into the priority queue
            public int compare(State o1, State o2) {
                return o1.getWeight() - o2.getWeight();
            }
        });

        times = 0;
        
        //intialize the distance of the current state to be 0
        dist.put(stringify(current), 0);

        //add the current state to the front of the states queue
        q.add(new State(current, 0));

        //A* Algorithm
        while(!q.isEmpty()){
            State crnt = q.poll();
            times++;
            if(Arrays.equals(crnt.getBoard(), finalBoard)) break;        //achieve the goal    
            for(State child : crnt.getNextStates()){
                if(dist.getOrDefault(stringify(child.getBoard()), Integer.MAX_VALUE) > child.getCost()){                    
                    parent.put(stringify(child.getBoard()), crnt.getBoard());
                    dist.put(stringify(child.getBoard()), child.getCost());
                    q.add(child);
                }
            }
        }
        return parent;
    }
}

class BoardControl{
    public static enum MOVES{UP, DOWN, RIGHT, LEFT};
    public static final byte[] GOAL = {1, 2, 3, 4, 5, 6, 7, 8, 0};

    public static int getBlankIndex(byte[] board){         //get the index of 0
        for(int i = 0 ; i < board.length ; ++i) if(board[i] == 0) return i;
        return -1;
    }

    public static void swap(byte[] board, int i, int j){   //swap two numbers
        byte iv = board[i];
        byte jv = board[j];
        board[i] = jv;
        board[j] = iv;
    }

    public static void print(byte[] b){                //print the board
        for(int i = 0 ; i < b.length ; i++){
            System.out.print(b[i] + " ");
            if ((i+1) % 3 == 0){
                System.out.print("\r\n");
            }
        } 
        System.out.println("");
    }

    public static void move(byte[] board, MOVES toMove){
        int blank = getBlankIndex(board);
        if(blank == -1) return;  //impossible, but just to be sure
        switch(toMove){
            case UP:
                if(blank / 3 != 0) swap(board, blank, blank-3);
                break;
            case DOWN:
                if(blank / 3 != 2) swap(board, blank, blank+3);
                break;
            case RIGHT:
                if(blank % 3 != 2) swap(board, blank, blank+1);
                break;
            case LEFT:
                if(blank % 3 != 0) swap(board, blank, blank-1);
                break;
        }
    }

    private String make(byte[] arr){
        String str = "";
        for(int i = 0 ; i < arr.length ; ++i){
            str += String.valueOf(arr[i]);
        }
        return str;
    }

    public void solve(byte[] board){
        Map<String, byte[]> parent = null;

        parent = Solvers.aStar(board.clone());            //store all {kid: parent} board
  
        //use backtracking like technique to get the moves to be made
        //solution states (not moves) are saved into the stack in order to be executed
        Stack<byte[]> nextBoard = new Stack<>();
        nextBoard.add(GOAL.clone());
        while(!Arrays.equals(nextBoard.peek(), board)){
            nextBoard.add(parent.get(make(nextBoard.peek())));   
        }   
        while(!nextBoard.empty()){
            print(nextBoard.pop());                       //print the path
        }
    }
}

public class A3_120090255 {
    public static void main(String[] args) throws Exception 
    {
        Scanner input = new Scanner(System.in);
        BoardControl a = new BoardControl();
        byte[] puzzle = new byte[9];
        for (int i = 0; i < 9; i++){
            puzzle[i] = input.nextByte();
        }

        a.solve(puzzle);
        input.close();
    }
}