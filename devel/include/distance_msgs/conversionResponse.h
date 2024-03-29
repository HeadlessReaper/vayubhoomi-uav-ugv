// Generated by gencpp from file distance_msgs/conversionResponse.msg
// DO NOT EDIT!


#ifndef DISTANCE_MSGS_MESSAGE_CONVERSIONRESPONSE_H
#define DISTANCE_MSGS_MESSAGE_CONVERSIONRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace distance_msgs
{
template <class ContainerAllocator>
struct conversionResponse_
{
  typedef conversionResponse_<ContainerAllocator> Type;

  conversionResponse_()
    : s(0.0)
    , success(false)  {
    }
  conversionResponse_(const ContainerAllocator& _alloc)
    : s(0.0)
    , success(false)  {
  (void)_alloc;
    }



   typedef float _s_type;
  _s_type s;

   typedef uint8_t _success_type;
  _success_type success;





  typedef boost::shared_ptr< ::distance_msgs::conversionResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::distance_msgs::conversionResponse_<ContainerAllocator> const> ConstPtr;

}; // struct conversionResponse_

typedef ::distance_msgs::conversionResponse_<std::allocator<void> > conversionResponse;

typedef boost::shared_ptr< ::distance_msgs::conversionResponse > conversionResponsePtr;
typedef boost::shared_ptr< ::distance_msgs::conversionResponse const> conversionResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::distance_msgs::conversionResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::distance_msgs::conversionResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::distance_msgs::conversionResponse_<ContainerAllocator1> & lhs, const ::distance_msgs::conversionResponse_<ContainerAllocator2> & rhs)
{
  return lhs.s == rhs.s &&
    lhs.success == rhs.success;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::distance_msgs::conversionResponse_<ContainerAllocator1> & lhs, const ::distance_msgs::conversionResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace distance_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::distance_msgs::conversionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::distance_msgs::conversionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::distance_msgs::conversionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::distance_msgs::conversionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::distance_msgs::conversionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::distance_msgs::conversionResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::distance_msgs::conversionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a10d50b2c9bbf69402cec6b79640e00c";
  }

  static const char* value(const ::distance_msgs::conversionResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa10d50b2c9bbf694ULL;
  static const uint64_t static_value2 = 0x02cec6b79640e00cULL;
};

template<class ContainerAllocator>
struct DataType< ::distance_msgs::conversionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "distance_msgs/conversionResponse";
  }

  static const char* value(const ::distance_msgs::conversionResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::distance_msgs::conversionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 s\n"
"bool success\n"
;
  }

  static const char* value(const ::distance_msgs::conversionResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::distance_msgs::conversionResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.s);
      stream.next(m.success);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct conversionResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::distance_msgs::conversionResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::distance_msgs::conversionResponse_<ContainerAllocator>& v)
  {
    s << indent << "s: ";
    Printer<float>::stream(s, indent + "  ", v.s);
    s << indent << "success: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.success);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DISTANCE_MSGS_MESSAGE_CONVERSIONRESPONSE_H
