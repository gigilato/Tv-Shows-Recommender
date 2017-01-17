package com.gm.gislain.tvshowapp.Model;

/**
 * Created by Gislain on 25/11/2016.
 */

public class Network {

    private int id;
    private String network;

    public static final String KEY_ID = "id";
    public static final String KEY_NETWORK = "network";

    public Network() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNetwork() {
        return network;
    }

    public void setNetwork(String network) {
        this.network = network;
    }
}
