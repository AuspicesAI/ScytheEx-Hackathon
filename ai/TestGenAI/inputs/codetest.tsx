// Importing necessary dependencies
import { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useAppDispatch } from '../../hooks/reduxHooks';
import { signin_text } from '../global/constants/constants';
import { Testimonials } from '../global/constants/TestimonialConstants';
import store from '../redux/store';
import useNavigation from '../global/utils/navigationUtils';
import './css/Signin.css';
import { login } from '../redux/auth/authActions';

// Validation schema using Yup library
const validationSchema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().required('Required'),
});

// Functional component for input fields
const AppInput: React.FC<any> = ({ type, ...props }) => {
  // Spread props and assign input type and styling
  return (
    <input
      type={type}
      {...props}
      required
      className="p-3 w-full my-0.5 border border-primary-black rounded-md shadow-sm bg-primary-white transition duration-300 hover:shadow text-primary-black focus:shadow focus:border-none focus:shadow-md"
    />
  );
};

// Functional component for Signin page
const Signin = () => {
  // Local state for error message and loading indicator
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Redux dispatch method
  const dispatch = useAppDispatch();

  // Navigation function
  const handleNavigation = useNavigation();

  // Side effect to change body style
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);

  // Formik form handling
  const formik = useFormik({
    // Set initial form values for email and password as empty strings
    initialValues: { email: '', password: '' },

    // Attach validation schema from Yup to enforce form field rules
    validationSchema,

    // Function that gets executed when the form is submitted
    onSubmit: async ({ email, password }) => {
      // Set the loading state to true, likely to show a spinner or disable the submit button
      setLoading(true);

      try {
        // Dispatch the login action and wait for it to complete
        // This should handle authentication on the server and set user information in the Redux store
        await dispatch(login(email, password));

        // Get the latest 'auth' state from Redux store
        const { auth } = store.getState();

        // Check if the user is authenticated
        // console.log(auth.isAuthenticated);
        if (auth.isAuthenticated) {
          // Log success message for debugging
          // console.log('Sign in successful');

          // Redirect the user to the UserDashboard route
          handleNavigation('/UserDashboard');
        }

        // Display any error messages received during the authentication process
        // If no error message exists, set a generic one
        setErrorMessage(auth.error ?? 'An unknown error has occurred.');
      } catch (error) {
        // Set an error message if any exceptions occur during the try block
        setErrorMessage('An unknown error has occurred. Please try again');
      } finally {
        // Reset the loading state to false, stopping any loading indicators
        setLoading(false);
      }
    },
  });

  return (
    <div id="signin-body">
      <div className="signin-container">
        <div className="max-w-[650px] mx-auto items-center justify-center h-full flex flex-col gap-2 bg-primary-white p-10 lg:rounded-l-2xl relative">
          <div className="text-center w-full">
            <label className="text-xl font-bold text-primary-purple">
              Welcome Back
            </label>
            <p className="text-14 text-gray-600 mt-3 mb-5">{signin_text}</p>
          </div>

          <form onSubmit={formik.handleSubmit} className="w-full">
            <div className="mb-2 w-full">
              <AppInput
                placeholder="Email"
                type="email"
                name="email"
                value={formik.values.email}
                onChange={formik.handleChange}
              />
            </div>

            <div className="mb-10 relative w-full">
              <AppInput
                placeholder="Password"
                type="password"
                name="password"
                value={formik.values.password}
                onChange={formik.handleChange}
              />
              <div className="text-red-600 lg:text-md pt-2 font-medium">
                {errorMessage}
              </div>
            </div>

            <div className="flex items-center justify-center w-full">
              <button className="button purple sign" type="submit">
                <span>Sign In</span>
              </button>
            </div>
          </form>

          <p className="text-center lg:text-md sm:text-xs text-gray-600 mt-2 w-full">
            Don't have an account?{' '}
            <a
              className="text-primary-purple no-underline transition-color duration-300 hover:text-blue-500 cursor-pointer"
              onClick={() => handleNavigation('/register')}
            >
              Sign Up
            </a>
            <br />
            {/*
<a
  className="text-primary-purple no-underline transition-color duration-300 hover:text-blue-500"
  onClick={() => handleNavigation('#')}
>
  Terms of use &amp; Conditions
</a>
*/}
          </p>
        </div>

        <div className="signin-testimonial">
          <p className="text-center text-lg font-semibold text-primary-purple">
            {Testimonials[1].text}
          </p>
          <img
            src={Testimonials[1].writerImage}
            alt="Logo"
            className="w-36 h-36 rounded-full bg-opacity-10 bg-black"
          />
          <div className="flex flex-col items-center justify-center gap-3">
            <span className="text-center text-lg font-semibold text-secondary-100">
              {Testimonials[1].name}
            </span>
            <span className="text-center text-s font-semibold text-primary-purple">
              {Testimonials[1].position}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signin;
