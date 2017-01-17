package com.gm.gislain.tvshowapp.Model;

/**
 * Created by Gislain on 25/11/2016.
 */

public class User {

    public static final String KEY_ID = "id";
    public static final String KEY_PASSWORD = "password";
    public static final String KEY_LOGIN = "login";

    private int id;
    private String login;
    private String password;

    public User() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
