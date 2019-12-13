package com.example.phoneaccelerometer;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    MainActivity activity ;
    ServerSocket serverSocket ;
    String message = "";
    static final int socketServerPORT = 2000 ;

    public Server(MainActivity activity) {
        this.activity = activity ;
        Thread socketServerThread = new Thread(new SocketServerThread());
        socketServerThread.start();
    }

    public int getPort() {
        return socketServerPORT ;
    }

    public void onDestroy () {
        if (serverSocket != null) {
            try {
                serverSocket.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private class SocketServerThread extends Thread {
        int count = 0;

        @Override
        public void run() {

            try {
                serverSocket = new ServerSocket(socketServerPORT);

                while (true) {
                    final Socket socket = serverSocket.accept();
                    count++;

                    SocketServerReplyThread socketServerReplyThread =
                            new SocketServerReplyThread(socket, count);
                    socketServerReplyThread.run();
                }
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private class SocketServerReplyThread extends Thread {
        private Socket hostThreadSocket ;
        int cnt ;

        SocketServerReplyThread(Socket socket, int c) {
            hostThreadSocket = socket ;
            cnt = c;
        }

        @Override
        public void run() {
            OutputStream outputStream ;

            try {
                outputStream = hostThreadSocket.getOutputStream();
                PrintStream printStream = new PrintStream(outputStream);
                while (true) {
                    printStream.println(activity.x + "\n" +
                            activity.y + "\n" +
                            activity.z  + "\n");
                    sleep(1000);
                }
//                printStream.close();

            }
            catch (IOException e) {
                e.printStackTrace();
                message += "Something wrong! " + e.toString() + "\n";
            }
            catch (InterruptedException e) {
                e.printStackTrace();
                message += "Something wrong! " + e.toString() + "\n";
            }

            activity.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    activity.msg.setText(message);
                }
            });
        }
    }

}
