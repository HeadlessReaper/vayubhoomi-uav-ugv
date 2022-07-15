// Auto-generated. Do not edit!

// (in-package distance_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let sensor_msgs = _finder('sensor_msgs');

//-----------------------------------------------------------

class dist_info {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.dist = null;
      this.mno = null;
      this.mname = null;
    }
    else {
      if (initObj.hasOwnProperty('dist')) {
        this.dist = initObj.dist
      }
      else {
        this.dist = new sensor_msgs.msg.Range();
      }
      if (initObj.hasOwnProperty('mno')) {
        this.mno = initObj.mno
      }
      else {
        this.mno = 0;
      }
      if (initObj.hasOwnProperty('mname')) {
        this.mname = initObj.mname
      }
      else {
        this.mname = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type dist_info
    // Serialize message field [dist]
    bufferOffset = sensor_msgs.msg.Range.serialize(obj.dist, buffer, bufferOffset);
    // Serialize message field [mno]
    bufferOffset = _serializer.int32(obj.mno, buffer, bufferOffset);
    // Serialize message field [mname]
    bufferOffset = _serializer.string(obj.mname, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type dist_info
    let len;
    let data = new dist_info(null);
    // Deserialize message field [dist]
    data.dist = sensor_msgs.msg.Range.deserialize(buffer, bufferOffset);
    // Deserialize message field [mno]
    data.mno = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [mname]
    data.mname = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += sensor_msgs.msg.Range.getMessageSize(object.dist);
    length += _getByteLength(object.mname);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'distance_msgs/dist_info';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9437189fa374886e3521594bcfcd5828';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    sensor_msgs/Range dist
    int32 mno
    string mname
    ================================================================================
    MSG: sensor_msgs/Range
    # Single range reading from an active ranger that emits energy and reports
    # one range reading that is valid along an arc at the distance measured. 
    # This message is  not appropriate for laser scanners. See the LaserScan
    # message if you are working with a laser scanner.
    
    # This message also can represent a fixed-distance (binary) ranger.  This
    # sensor will have min_range===max_range===distance of detection.
    # These sensors follow REP 117 and will output -Inf if the object is detected
    # and +Inf if the object is outside of the detection range.
    
    Header header           # timestamp in the header is the time the ranger
                            # returned the distance reading
    
    # Radiation type enums
    # If you want a value added to this list, send an email to the ros-users list
    uint8 ULTRASOUND=0
    uint8 INFRARED=1
    
    uint8 radiation_type    # the type of radiation used by the sensor
                            # (sound, IR, etc) [enum]
    
    float32 field_of_view   # the size of the arc that the distance reading is
                            # valid for [rad]
                            # the object causing the range reading may have
                            # been anywhere within -field_of_view/2 and
                            # field_of_view/2 at the measured range. 
                            # 0 angle corresponds to the x-axis of the sensor.
    
    float32 min_range       # minimum range value [m]
    float32 max_range       # maximum range value [m]
                            # Fixed distance rangers require min_range==max_range
    
    float32 range           # range data [m]
                            # (Note: values < range_min or > range_max
                            # should be discarded)
                            # Fixed distance rangers only output -Inf or +Inf.
                            # -Inf represents a detection within fixed distance.
                            # (Detection too close to the sensor to quantify)
                            # +Inf represents no detection within the fixed distance.
                            # (Object out of range)
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new dist_info(null);
    if (msg.dist !== undefined) {
      resolved.dist = sensor_msgs.msg.Range.Resolve(msg.dist)
    }
    else {
      resolved.dist = new sensor_msgs.msg.Range()
    }

    if (msg.mno !== undefined) {
      resolved.mno = msg.mno;
    }
    else {
      resolved.mno = 0
    }

    if (msg.mname !== undefined) {
      resolved.mname = msg.mname;
    }
    else {
      resolved.mname = ''
    }

    return resolved;
    }
};

module.exports = dist_info;
