package com.bg_client.packer;

import android.content.pm.PackageManager;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;

import java.util.HashMap;
import java.util.Map;

import javax.annotation.Nullable;

/**
 * Created by frank on 2017/4/17.
 */

public class ChannelInfo extends ReactContextBaseJavaModule {

    public ChannelInfo(ReactApplicationContext reactContext) {
        super(reactContext);
    }



    @Nullable
    @Override
    public Map<String, Object> getConstants() {
        Map<String, Object> constants = new HashMap<String, Object>();
        try {
            constants.put("CHANNEL", getReactApplicationContext().getPackageManager().getApplicationInfo(getReactApplicationContext().getPackageName(), PackageManager.GET_META_DATA).metaData.getString("CHANNEL_NAME"));
        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
        };
        return constants;
    }

    @Override
    public String getName() {
        return "ChannelPackage";
    }
}
