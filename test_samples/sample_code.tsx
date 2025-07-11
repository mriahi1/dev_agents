import React, { useState, useEffect } from 'react';

// Example component with various issues for testing

export const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Missing cleanup in useEffect
  useEffect(() => {
    console.log('Fetching user data'); // Console log
    
    const fetchUser = async () => {
      // Hardcoded API key (security issue)
      const apiKey = 'sk_live_1234567890abcdef';
      
      // SQL injection vulnerability
      const query = `SELECT * FROM users WHERE id = ${userId}`;
      
      try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error('Error:', error); // Another console log
      } finally {
        setLoading(false);
      }
    };
    
    fetchUser();
    
    // Missing cleanup for event listener
    window.addEventListener('resize', handleResize);
  }, [userId]);
  
  // Complex function (high cyclomatic complexity)
  const processUserData = (data) => {
    if (!data) return null;
    if (data.type === 'admin') {
      if (data.permissions.includes('write')) {
        if (data.department === 'IT') {
          if (data.level > 5) {
            if (data.active) {
              return 'Super Admin';
            } else {
              return 'Inactive Admin';
            }
          } else {
            return 'Junior Admin';
          }
        } else {
          return 'Department Admin';
        }
      } else {
        return 'Read Only Admin';
      }
    } else if (data.type === 'user') {
      if (data.verified) {
        return 'Verified User';
      } else {
        return 'Unverified User';
      }
    } else {
      return 'Unknown';
    }
  };
  
  // Missing memoization for expensive operation
  const sortedPosts = user?.posts?.sort((a, b) => b.date - a.date);
  
  // Inline event handler (causes re-renders)
  const handleClick = () => {
    alert('Clicked!');
  };
  
  // TODO: Implement user avatar upload
  // FIXME: Handle edge case when user has no posts
  
  // Very long line that exceeds 120 characters - this is a really long comment that should be broken up into multiple lines for better readability
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return (
    <div className="user-profile">
      {/* Missing alt text on image */}
      <img src={user?.avatar} />
      
      {/* Dangerous HTML (XSS vulnerability) */}
      <div dangerouslySetInnerHTML={{ __html: user?.bio }} />
      
      {/* Non-semantic clickable div */}
      <div onClick={handleClick}>Click me</div>
      
      {/* Missing key in list */}
      {sortedPosts?.map(post => (
        <div className="post">
          <h3>{post.title}</h3>
          <p>{post.content}</p>
        </div>
      ))}
      
      {/* Form input without label */}
      <input type="text" placeholder="Search..." />
      
      {/* Low contrast text color */}
      <p style={{ color: '#e0e0e0' }}>Some light gray text</p>
      
      {/* Focus outline removed without alternative */}
      <button style={{ outline: 'none' }}>No Focus Indicator</button>
    </div>
  );
};

// Another component to test more issues
const handleResize = () => {
  // Using eval (security issue)
  eval('window.width = ' + window.innerWidth);
};

// Insecure random for token generation
const generateToken = () => {
  return Math.random().toString(36).substring(7); // Insecure for tokens
};

// Large function (over 50 lines)
const processOrder = (order) => {
  // Line 1
  if (!order) {
    return null;
  }
  // Line 4
  const items = order.items;
  const shipping = order.shipping;
  const billing = order.billing;
  const customer = order.customer;
  // Line 9
  let total = 0;
  let subtotal = 0;
  let tax = 0;
  let discount = 0;
  // Line 14
  for (const item of items) {
    subtotal += item.price * item.quantity;
  }
  // Line 17
  if (order.discountCode) {
    if (order.discountCode === 'SAVE10') {
      discount = subtotal * 0.1;
    } else if (order.discountCode === 'SAVE20') {
      discount = subtotal * 0.2;
    }
  }
  // Line 24
  subtotal = subtotal - discount;
  // Line 26
  if (shipping.country === 'US') {
    if (shipping.state === 'CA') {
      tax = subtotal * 0.0875;
    } else if (shipping.state === 'NY') {
      tax = subtotal * 0.08;
    } else {
      tax = subtotal * 0.06;
    }
  } else {
    tax = 0;
  }
  // Line 37
  total = subtotal + tax + shipping.cost;
  // Line 39
  const result = {
    items: items,
    subtotal: subtotal,
    discount: discount,
    tax: tax,
    shipping: shipping.cost,
    total: total,
    customer: customer,
    billing: billing,
    shipping: shipping,
    status: 'processed',
    processedAt: new Date()
  };
  // Line 52
  return result;
  // Line 54 - This function is too long!
}; 